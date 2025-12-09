import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from litestar import Litestar
from litestar.di import Provide
from user_controller import UserController
from user_repository import UserRepository
from user_service import UserService
from models import Base, User, Address, Order  # Импорт моделей из models.py

# --- Настройка базы данных и асинхронного движка ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/test_db")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# --- Провайдеры зависимостей ---
async def provide_db_session() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)

async def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)

# --- Инициализация приложения ---
app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
    },
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)