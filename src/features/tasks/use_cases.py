from typing import List
from fastapi import Depends
from .schemas import TaskCreate, TaskRead
from .services import TaskService
from src.features.users import UserService
from src.shared.uow import UnitOfWork, get_uow


class TaskUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.task_service = TaskService(uow.session)
        self.user_service = UserService(uow.session)

    async def get_all(self):
        async with self.uow:
            return await self.task_service.get_all()

    async def create_task(self, task_in: TaskCreate):
        async with self.uow:
            # if task_in.assignee_id:
            #     user = await self.user_service.get_by_id(task_in.assignee_id)
            #     if not user:
            #         raise ValueError("Assignee User not found")
            return await self.task_service.create_task(task_in)

    async def delete_task(self, task_id: int):
        async with self.uow:
            return await self.task_service.delete_task(task_id)

    async def get_by_creater(self, creator_id: int) -> List[TaskRead]:
        async with self.uow:
            return await self.task_service.get_by_creater(creator_id)

    async def get_by_assigned(self, assignee_id: int) -> List[TaskRead]:
        async with self.uow:
            return await self.task_service.get_by_assigned(assignee_id)


def get_task_use_case(uow: UnitOfWork = Depends(get_uow)):
    return TaskUseCase(uow)
