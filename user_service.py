from user_repository import UserRepository
from schemas import UserCreate, UserUpdate  
from models import User
from uuid import UUID
from typing import List, Optional

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repository.get_by_id(session=None, user_id=user_id)

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[User]:
        return await self.user_repository.get_by_filter(session=None, count=count, page=page, **kwargs)

    async def create(self, user_data: UserCreate) -> User:
        return await self.user_repository.create(session=None, user_data=user_data)

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User:
        return await self.user_repository.update(session=None, user_id=user_id, user_data=user_data)

    async def delete(self, user_id: UUID) -> None:
        await self.user_repository.delete(session=None, user_id=user_id)

    async def get_total_count(self) -> int:
        return await self.user_repository.count()