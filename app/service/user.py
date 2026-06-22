from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import create_access_token, verify_password
from app.repository.user import UserRepository
from app.schemas.schemas import UserCreate, UserResponse, Token
from config import settings


class UserService:
    @classmethod
    async def add_user(cls,user: UserCreate, session: AsyncSession) -> UserResponse:
        if await UserRepository.get_user_by_login(user.login, session):
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = await UserRepository.add_user(user, session)
        if new_user is None:
            raise HTTPException(status_code=400, detail="User already exists")
        await session.commit()
        return UserResponse(login=new_user.login, role=new_user.role)




class AuthService:
    @classmethod
    async def login_for_access_token(
            cls,
            login: str,
            password: str,
            session: AsyncSession
    ):
        user = await UserRepository.get_user_by_login(login, session)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")