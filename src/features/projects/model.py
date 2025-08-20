from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, String, Boolean, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)

    # связь "многие проекты → один пользователь"
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    creator: Mapped["User"] = relationship(back_populates="created_projects")

    # связь "один проект → много задач"
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}')>"
