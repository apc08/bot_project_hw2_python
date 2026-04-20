from pydantic import BaseModel, EmailStr

# схема для регистрации
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

# схема для токена
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
