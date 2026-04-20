from jose import JWTError, jwt, ExpiredSignatureError
from app.core.config import settings
from app.core.exceptions import TokenExpiredError, TokenInvalidError


# декодирование и проверка jwt токена
def decode_and_validate(token):
    try:
        # декодируем токен
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )

        # проверка обязательного поля
        if "sub" not in payload:
            raise TokenInvalidError("Token missing required feild: sub")

        return payload

    except ExpiredSignatureError:
            raise TokenExpiredError("Authentication token expired")
    except JWTError as e:
             raise TokenInvalidError(f"Invalid authentication token: {str(e)}")
