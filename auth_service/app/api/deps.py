from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.security import decode_token
from app.core.exceptions import InvalidTokenError
from app.db.session import AsyncSessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# получение сессии бд
async def get_session():
    
    async with AsyncSessionLocal() as session:

        yield session

# проверка тоекна
async def get_current_user_id(token:str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
    except JWTError:
        raise InvalidTokenError("Invalid token")

    user_id = payload.get("sub")
    return int(user_id)
