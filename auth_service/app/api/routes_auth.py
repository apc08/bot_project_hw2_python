from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_session, get_current_user_id
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase

router = APIRouter()

 # регистрация
@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session)
    auth_usecase = AuthUseCase(user_repo)
    user = await auth_usecase.register(email=data.email, password=data.password)
    return user


# логин

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session)
    auth_usecase = AuthUseCase(user_repo)
    token = await auth_usecase.login(email=form_data.username, password=form_data.password)
    return TokenResponse(access_token=token)

# получить профиль
@router.get("/me", response_model=UserPublic)
async def get_me(user_id: int = Depends(get_current_user_id),
                session: AsyncSession = Depends(get_session)):
        user_repo = UserRepository(session)
        auth_usecase = AuthUseCase(user_repo)
        user = await auth_usecase.get_profile(user_id)
        return user
