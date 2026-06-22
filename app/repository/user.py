from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.booking import User
from app.schemas.schemas import UserCreate


class UserRepository:
    @classmethod
    async def add_user(cls, data: UserCreate, session: AsyncSession) -> User | None:

        user = User(
            login=data.login,
            password_hash=hash_password(data.password),
            role="employee",
        )
        session.add(user)
        await session.flush()
        return user

    @classmethod
    async def get_user_by_id(cls, user_id: int, session: AsyncSession):
        return await session.scalar(select(User).where(User.id == user_id))

    @classmethod
    async def get_user_by_login(cls, login: str, session: AsyncSession):
        return await session.scalar(select(User).where(User.login == login))