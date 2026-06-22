import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import create_test_user, login_user, create_test_room, auth_header


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/users",
        json={"login":"test_user", "password":"test_password"},
    )

    assert response.status_code == 201
    assert response.json()["login"] == "test_user"


@pytest.mark.asyncio
async def test_create_user_error(client: AsyncClient):
    response = await client.post(
        "/users",
        json={"password":""},
    )
    assert response.status_code == 422
    assert "login" in response.text


@pytest.mark.asyncio
async def test_create_user_same_login(client: AsyncClient):
    await client.post(
        "/users",
        json={"login":"test_user", "password":""},
    )

    response = await client.post(
        "/users",
        json={"login":"test_user", "password":""},
    )

    assert response.status_code == 400
    



@pytest.mark.asyncio
async def test_employee_cannot_access_admin_endpoint(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    response = await client.get(
        "/admin/bookings",
        headers=headers,
    )

    assert response.status_code == 403


