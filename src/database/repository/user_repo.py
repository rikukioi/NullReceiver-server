from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User
from src.schemas import UserInDatabase


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def username_exists(self, username: str) -> bool:
        query = await self.session.execute(
            select(User).where(User.username == username)
        )
        return query.scalar_one_or_none() is not None

    async def get_user(self, username: str) -> UserInDatabase | None:
        query = await self.session.execute(
            select(User).where(User.username == username)
        )
        model = query.scalar_one_or_none()

        if model is not None:
            return UserInDatabase.model_validate(model)
        else:
            return None

    def add_in_session(self, username: str, hashed_pass: bytes) -> None:
        model = User(
            username=username,
            password=hashed_pass,
        )
        self.session.add(model)
