from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.features.users.models import User
    from src.features.projects.model import Project


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), nullable=False
    )

    # исполнитель задачи
    assignee_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    assignee: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[assignee_id], back_populates="assigned_tasks"
    )

    # автор задачи
    creator_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    creator: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[creator_id], back_populates="created_tasks"
    )

    # проект задачи
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=False
    )
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', assignee_id={self.assignee_id})>"
