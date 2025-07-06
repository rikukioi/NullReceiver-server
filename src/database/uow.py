from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from .session import AsyncSessionLocal


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()


@asynccontextmanager
async def get_auto_session() -> AsyncGenerator[UnitOfWork, None]:
    async with AsyncSessionLocal() as session:
        async with UnitOfWork(session) as uow:
            yield uow
