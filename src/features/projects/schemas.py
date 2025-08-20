from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict

from src.shared.base_schema import BaseSchema
from src.features.tasks.schemas import TaskRead


class ProjectBase(BaseSchema):
    title: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    creator_id: int  # TODO убрать, заменить на current_user
    pass


class ProjectUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    pass


class ProjectRead(ProjectBase):
    id: int
    completed: bool
    created_at: datetime
    creator_id: int


class ProjectWithTasksRead(ProjectRead):
    tasks: List[TaskRead] | None = None
