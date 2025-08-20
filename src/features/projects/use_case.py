from typing import List

from fastapi import Depends
from src.features.projects.schemas import ProjectCreate, ProjectRead
from src.features.projects.services import ProjectService
from src.features.tasks.services import TaskService
from src.shared.uow import UnitOfWork, get_uow


class ProjectUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.project_service = ProjectService(uow.session)
        self.task_service = TaskService(uow.session)

    async def get_all(self):
        async with self.uow:
            return await self.project_service.get_all()

    async def create_task(self, project_in: ProjectCreate):
        async with self.uow:
            return await self.project_service.create_project(project_in)

    async def delete_task(self, project_id: int):
        async with self.uow:
            return await self.project_service.delete_project(project_id)

    async def get_by_creator(self, creator_id: int) -> List[ProjectRead]:
        async with self.uow:
            return await self.project_service.get_by_creator(creator_id)


def get_project_use_case(uow: UnitOfWork = Depends(get_uow)):
    return ProjectUseCase(uow)
