from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# путь к базе
DATABASE_URL = f"sqlite+aiosqlite:///{settings.sqlite_path}"

# engine для  подключения
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)


# сессии
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)
