from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings



#  bcrypt для паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(sub:int, role:str) -> str:
    # время жизни токена
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(sub),
        "role": role,
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


# декодирование токена
def decode_token(token: str) -> dict:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )
        return payload
