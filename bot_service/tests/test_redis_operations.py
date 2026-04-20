import pytest
from app.infra.redis_operations import (
    save_user_token,
    get_user_token,
    delete_user_token,
    get_llm_result,
    delete_llm_result,
)


@pytest.mark.asyncio
async def test_save_and_get_user_token(mock_settings, fake_redis):
    user_id = 12345
    token = "test_jwt_token"

    await save_user_token(user_id, token)
    result = await get_user_token(user_id)

    assert result is not None
    assert result.decode('utf-8') == token


@pytest.mark.asyncio
async def test_get_nonexistent_token(mock_settings, fake_redis):
    user_id = 99999
    result = await get_user_token(user_id)
    assert result is None


@pytest.mark.asyncio
async def test_delete_user_token(mock_settings, fake_redis):
    user_id = 12345
    token = "test_jwt_token"

    await save_user_token(user_id, token)
    await delete_user_token(user_id)

    result = await get_user_token(user_id)
    assert result is None


@pytest.mark.asyncio
async def test_get_llm_result(mock_settings, fake_redis):
    user_id = 12345
    task_id = "test-task-123"
    result_text = "This is LLM response"

    key = f"llm_result:{user_id}:{task_id}"
    await fake_redis.set(key, result_text)

    result = await get_llm_result(user_id, task_id)

    assert result is not None
    assert result.decode('utf-8') == result_text


@pytest.mark.asyncio
async def test_get_nonexistent_llm_result(mock_settings, fake_redis):
    user_id = 99999
    task_id = "nonexistent-task"

    result = await get_llm_result(user_id, task_id)
    assert result is None


@pytest.mark.asyncio
async def test_delete_llm_result(mock_settings, fake_redis):
    user_id = 12345
    task_id = "test-task-123"
    result_text = "This is LLM response"

    key = f"llm_result:{user_id}:{task_id}"
    await fake_redis.set(key, result_text)

    await delete_llm_result(user_id, task_id)

    result = await get_llm_result(user_id, task_id)
    assert result is None
