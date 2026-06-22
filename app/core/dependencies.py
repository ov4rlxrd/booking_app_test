from typing import Annotated

from fastapi import Depends, HTTPException

from app.core.security import verify_access_token, oauth2_scheme
from app.database import SessionDep
from app.models.booking import User
from app.repository.user import UserRepository


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: SessionDep
) -> User:
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await UserRepository.get_user_by_id(user_id_int, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def role_checker(allowed_roles: list[str]):
    async def checker(current_user: CurrentUser) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user
    return checker

AdminUser = Annotated[User, Depends(role_checker(["admin"]))]