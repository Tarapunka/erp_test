from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func


# Дженерик-типы
T = TypeVar("T")  # SQLAlchemy модель
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseRepository(Generic[T, CreateSchema, UpdateSchema]):
    """
    Базовый асинхронный репозиторий c CRUD-операциями.
    Не занимается загрузкой связей — это задача сервиса.
    """

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.model = model
        self.session = session

    async def get_by_id(self, id: int) -> Optional[T]:
        """Получить объект по ID"""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Получить список c пагинацией"""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_fields(self, **kwargs) -> Optional[T]:
        """Получить один объект по произвольным полям"""
        stmt = select(self.model)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(self, obj_in: CreateSchema) -> T:
        """Создать новый объект из Pydantic-схемы"""
        db_obj = self.model(**obj_in.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(
        self, id: int, obj_in: UpdateSchema | Dict[str, Any]
    ) -> Optional[T]:
        """
        Обновить объект по ID.
        Принимает либо Pydantic-схему, либо словарь.
        Использует ORM-объект для гарантии совместимости (включая SQLite).
        """
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None

        # Преобразуем входные данные в словарь
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # Обновляем поля
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> bool:
        """Удалить объект по ID"""
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        """Получить общее количество записей"""
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()

    async def exists(self, id: int) -> bool:
        """Проверить, существует ли объект с таким ID"""
        stmt = select(self.model.id).where(self.model.id == id).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None
