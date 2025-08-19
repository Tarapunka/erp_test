from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TaskCreate, TaskRead

from .repository import TaskRepository


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)

    async def create_task(self, task_in: TaskCreate) -> TaskRead:
        task_out = await self.repo.create(task_in)
        return TaskRead.model_validate(task_out)

    async def get_all(self) -> List[TaskRead]:
        tasks = await self.repo.get_all()
        return [TaskRead.model_validate(task) for task in tasks]

    async def delete_task(self, task_id: int) -> bool:
        return await self.repo.delete(task_id)

    async def get_by_creater(self, creator_id: int) -> List[TaskRead]:
        tasks = await self.repo.get_by_creater(creator_id)
        return [TaskRead.model_validate(task) for task in tasks]

    async def get_by_assigned(self, assignee_id: int) -> List[TaskRead]:
        tasks = await self.repo.get_by_assigned(assignee_id)
        return [TaskRead.model_validate(task) for task in tasks]
