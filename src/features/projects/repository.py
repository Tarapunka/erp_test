from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.projects.model import Project
from src.features.projects.schemas import (
    ProjectCreate,
    ProjectUpdate,
)
from src.shared.base_repository import BaseRepository


class ProjectRepository(BaseRepository[Project, ProjectCreate, ProjectUpdate]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Project)

    async def get_by_creator(self, creator_id: int) -> List[Project]:
        stmt = select(Project).where(Project.creator_id == creator_id)
        project = await self.session.execute(stmt)
        return list(project.scalars().all())
