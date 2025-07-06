from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repository import UserRepository

from .session import AsyncSessionLocal


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(self.session)

    async def __aenter__(self):
        await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()


async def get_auto_session() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(AsyncSessionLocal()) as uow:
        yield uow
