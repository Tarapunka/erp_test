# app/shared/uow.py
from abc import ABC, abstractmethod
from typing import Callable
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.database import get_async_session


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session is None:
            return

        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.session.close()

    async def commit(self):
        if self.session is not None:
            await self.session.commit()

    async def rollback(self):
        if self.session is not None:
            await self.session.rollback()


async def get_uow(session: AsyncSession = Depends(get_async_session)):
    return UnitOfWork(session=session)
