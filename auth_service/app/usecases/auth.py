from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError
    )

from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UserRepository


class AuthUseCase:
    def __init__(self, user_repo:UserRepository):
        self.user_repo = user_repo

    # регистрация
    async def register(self, email:str, password:str):
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise UserAlreadyExistsError("Email already registered")

        password_hash = hash_password(password)
        user = await self.user_repo.create(
            email=email,
            password_hash=password_hash
        )
        return user



    async def login(self, email:str, password:str) -> str:
        # проверка пользователя
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise InvalidCredentialsError("Invalid email or password")

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")

        token = create_access_token(sub=user.id, role=user.role)
        return token


    async def get_profile(self, user_id:int):
        user = await self.user_repo.get_by_id(user_id)
        if not user:
                raise UserNotFoundError("User not found")
        return user
