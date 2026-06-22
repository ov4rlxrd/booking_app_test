from datetime import timedelta, datetime

import pytest
from fastapi import HTTPException

from app.core.dependencies import role_checker
from app.core.security import verify_password, hash_password, create_access_token, verify_access_token
from app.models.booking import User
from app.schemas.schemas import CreateBooking, UserCreate


def test_hash_password_and_verify():
    password = "test"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("test1", hashed_password)

def test_create_access_token_contains_correct_sub():
    token = create_access_token(data={"sub": "1"}, expires_delta=timedelta(minutes=5))
    user_id = verify_access_token(token)
    assert user_id == "1"


@pytest.mark.asyncio
async def test_role_checker():
    checker = role_checker(["admin"])
    fake_admin = User(id=1, login="admin", password_hash="x", role="admin")
    fake_employee = User(id=2, login="emp", password_hash="x", role="employee")


    result = await checker(fake_admin)

    with pytest.raises(HTTPException) as ex:
        await checker(fake_employee)

    assert result == fake_admin
    assert ex.value.status_code == 403


def test_create_booking_schema():
    data = CreateBooking(room_slot_id=1, date="2026-06-20")
    assert data.room_slot_id == 1

def test_create_user_schema():
    user = UserCreate(login="User", password="password")

    assert user.login == "User"
    assert user.password == "password"