from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Task
from .schemas import TaskCreate, TaskUpdate
from src.shared.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task, TaskCreate, TaskUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Task)

    async def get_by_creater(self, sreater_id: int) -> List[Task]:
        stmt = select(Task).where(Task.creator_id == sreater_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_assigned(self, assignee_id: int) -> List[Task]:
        stmt = select(Task).where(Task.assignee_id == assignee_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
