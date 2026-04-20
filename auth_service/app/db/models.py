from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base


class User(Base):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)  # уникальный емейл
    password_hash = Column(String(255))
    role = Column(String(50), default="user")  # роль пользователя
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
