import asyncio
import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.core.jwt import decode_and_validate
from app.core.exceptions import TokenExpiredError, TokenInvalidError
from app.infra.redis_operations import (
    save_user_token,
    get_user_token,
    delete_user_token,
    get_llm_result,
    delete_llm_result,
)
from app.tasks.llm_tasks import llm_request

logger = logging.getLogger(__name__)

router = Router()


# команда старт
@router.message(Command("start"))
async def cmd_start(message: Message):
    # приветствие пользователя
    user = message.from_user
    text = (
        f"Привет,   {user.first_name}!\n\n"
        "Я бот для LLM-консультаций.\n\n"
        "Чтобы начать работу:\n"
        "1. Зарегистрируйтесь в Auth Service (http://localhost:8000/docs)\n"
        "2. Получите JWT токен через POST /auth/login\n"
        "3. Отправьте мне токен командой: /token [ваш_jwt]\n\n"
        "После этого вы сможете задавать мне вопросы!\n\n"
        "Команды:\n"
        "/token [jwt] - сохранить JWT токен\n"
        "/revoke - удалить сохранённый токен\n"
        "/help - показать эту справку"
    )
    await message.answer(text)


# сохранение токена
@router.message(Command("token"))
async def cmd_token(message: Message):
    user_id = message.from_user.id

    # проверка формата команды
    if not message.text or len(message.text.split()) < 2:
        await message.answer(
            "Использование: /token [ваш_jwt]\n\n"
            "Пример:\n"
            "/token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        )
        return

    token = message.text.split(maxsplit=1)[1].strip()

    # валидация и сохранение
    try:
        payload = decode_and_validate(token)
        logger.info(f"Token validated for user {user_id}: {payload.get('sub')}")

        await save_user_token(user_id, token)

        await message.answer(
            "Токен успешно сохранён!\n\n"
            "Теперь вы можете задавать мне вопросы. "
            "Просто отправьте сообщение."
        )

    except TokenExpiredError:
        await message.answer(
            "Токен истёк.\n\n"
            "Получите новый токен через Auth Service:\n"
            "POST http://localhost:8000/auth/login"
        )

    except TokenInvalidError as e:
        await message.answer(
            f"Невалидный токен.\n\n"
            f"Ошибка: {str(e)}\n\n"
            "Убедитесь, что вы скопировали токен полностью."
        )


# удаление токена
@router.message(Command("revoke"))
async def cmd_revoke(message: Message):
    user_id = message.from_user.id

    await delete_user_token(user_id)
    await message.answer(
        "Токен удалён.\n\n"
        "Для использования бота получите новый токен и отправьте /token [jwt]"
    )



# справка по командам
@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "Справка по командам:\n\n"
        "/start - приветствие и инструкция\n"
        "/token [jwt] - сохранить JWT токен\n"
        "/revoke - удалить сохранённый токен\n"
        "/help - эта справка\n\n"
        "После сохранения токена просто отправьте мне любой вопрос, "
        "и я обращусь к LLM для получения ответа."
    )
    await message.answer(text)


# обработка текстовых сообщений

@router.message()
async def handle_text_message(message:Message):
    user_id = message.from_user.id
    prompt = message.text

    if not prompt:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return

    # проверка наличия токена
    token_bytes = await get_user_token(user_id)
    if not token_bytes:
        await message.answer(
            "У вас нет сохранённого токена.\n\n"
            "Получите JWT через Auth Service и отправьте:\n"
            "/token [ваш_jwt]"
        )
        return

    token = token_bytes.decode('utf-8')

    # валидация
    try:
        decode_and_validate(token)
    except TokenExpiredError:
        await message.answer(
            "Ваш токен истёк.\n\n"
            "Получите новый токен через Auth Service и отправьте:\n"
            "/token [новый_jwt]"
        )
        await delete_user_token(user_id)
        return
    except TokenInvalidError:
        await message.answer(
            "Ваш токен невалиден.\n\n"
            "Получите новый токен и отправьте:\n"
            "/token [новый_jwt]"
        )
        await delete_user_token(user_id)
        return

    # отправка задачи в celery
    task = llm_request.delay(user_id, prompt)

    await message.answer(
        f"Обрабатываю ваш запрос...\n\n"
        f"Task ID: {task.id}\n\n"
        f"Это может занять до 60 секунд."
    )

    # запуск polling в фоне
    asyncio.create_task(poll_llm_result(message, task.id, user_id))


# polling результата из redis
async def poll_llm_result(
    message:Message,
    task_id:str,
    user_id:int
):
    for attempt in range(1, 31):
        await asyncio.sleep(2.0)

        result_bytes = await get_llm_result(user_id, task_id)

        if result_bytes:
            await delete_llm_result(user_id, task_id)
            text = result_bytes.decode('utf-8')

            # разбивка длинных сообщений
            if len(text) > 4096:
                for i in range(0, len(text), 4096):
                    chunk = text[i:i + 4096]
                    await message.answer(chunk)
            else:
                await message.answer(text)

            return

    await message.answer(
        "Превышено время ожидания ответа (60 секунд).\n\n"
        "Возможные причины:\n"
        "- LLM сервис перегружен\n"
        "- Ошибка при обработке запроса\n\n"
        "Попробуйте ещё раз или проверьте статус worker-а."
    )
