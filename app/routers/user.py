from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.core.dependencies import CurrentUser
from app.database import SessionDep
from app.schemas.schemas import UserResponse, UserCreate
from app.service.user import UserService, AuthService

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: SessionDep) -> UserResponse:
    new_user = await UserService.add_user(user, session)
    return new_user

@users_router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: SessionDep
):
    return await AuthService.login_for_access_token(login=form_data.username, password=form_data.password, session=session)

@users_router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user(current_user: CurrentUser) -> UserResponse:
    return current_user


