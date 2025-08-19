from fastapi import Depends
from src.features.users.schemas import UserCreate, UserUpdate
from src.features.users.services import UserService
from src.shared.uow import UnitOfWork, get_uow


class GetAllUsersUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.user_service = UserService(uow.session)

    async def execute(self):
        async with self.uow:
            return await self.user_service.get_all()


def get_user_list_use_case(uow: UnitOfWork = Depends(get_uow)):
    return GetAllUsersUseCase(uow)


class UserUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.user_service = UserService(uow.session)

    async def get_all(self):
        async with self.uow:
            return await self.user_service.get_all()

    async def get_by_id(self, user_id: int):
        async with self.uow:
            user = await self.user_service.get_by_id(user_id)
            return user

    async def create_user(self, user_in: UserCreate):
        async with self.uow:
            return await self.user_service.create_user(user_in)

    async def delete_user(self, user_id: int):
        async with self.uow:
            return await self.user_service.delete_user(user_id)

    async def update_user(self, user_id: int, user_in: UserUpdate):
        async with self.uow:
            return await self.user_service.update_user(user_id, user_in)


def get_user_use_case(uow: UnitOfWork = Depends(get_uow)):
    return UserUseCase(uow)
