from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    assignee_id: int | None = None


class TaskCreate(TaskBase):
    creator_id: int
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    completed: bool | None = None


class TaskRead(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    creator_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
