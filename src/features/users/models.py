from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean
from features.projects.model import Project
from src.features.tasks.models import Task
from src.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # проекты, созданные пользователем
    created_projects: Mapped[List["Project"]] = relationship(
        back_populates="creator", cascade="all, delete-orphan"
    )

    # задачи, назначенные пользователю
    assigned_tasks: Mapped[List["Task"]] = relationship(
        back_populates="assignee", foreign_keys="Task.assignee_id"
    )

    # задачи, созданные пользователем
    created_tasks: Mapped[List["Task"]] = relationship(
        back_populates="creator", foreign_keys="Task.creator_id"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"
