from litestar import Controller, get, post, delete, put
from litestar.di import Provide
from user_service import UserService
from schemas import UserCreate, UserUpdate, User, UserListResponse
from litestar.exceptions import NotFoundException
from typing import List
from uuid import UUID

def get_user_service() -> UserService:
    return UserService()

class UserController(Controller):
    path = "/users"
    dependencies = {"user_service": Provide(get_user_service, sync_to_thread=False)}

    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_id: int,
        user_service: UserService = Provide(get_user_service, sync_to_thread=False),
    ) -> User:
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} не найден")
        return User.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService = Provide(get_user_service, sync_to_thread=False),
    ) -> UserListResponse:
        users = await user_service.get_by_filter(count=100, page=1)
        total = await user_service.get_total_count()
        return UserListResponse(
            total=total,
            users=[User.model_validate(user) for user in users]
        )

    @post()
    async def create_user(
        self,
        user_data: UserCreate,
        user_service: UserService = Provide(get_user_service, sync_to_thread=False),
    ) -> User:
        user = await user_service.create(user_data)
        return User.model_validate(user)

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        user_id: int,
        user_service: UserService = Provide(get_user_service, sync_to_thread=False),
    ) -> None:
        await user_service.delete(user_id)

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_id: int,
        user_data: UserUpdate,
        user_service: UserService = Provide(get_user_service, sync_to_thread=False),
    ) -> User:
        user = await user_service.update(user_id, user_data)
        return User.model_validate(user)