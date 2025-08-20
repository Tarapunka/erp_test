from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.projects.repository import ProjectRepository
from src.features.projects.schemas import ProjectCreate, ProjectRead


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ProjectRepository(self.session)

    async def get_by_id(self, project_id: int) -> ProjectRead:
        project = await self.repo.get_by_id(project_id)
        return ProjectRead.model_validate(project)

    async def get_by_creator(self, creator_id: int) -> List[ProjectRead]:
        projects = await self.repo.get_by_creator(creator_id)
        return [ProjectRead.model_validate(project) for project in projects]

    async def get_all(self) -> List[ProjectRead]:
        projects = await self.repo.get_all()
        return [ProjectRead.model_validate(project) for project in projects]

    async def create_project(self, project_in: ProjectCreate) -> ProjectRead:
        project_out = await self.repo.create(project_in)
        return ProjectRead.model_validate(project_out)

    async def delete_project(self, project_id: int) -> bool:
        return await self.repo.delete(project_id)
