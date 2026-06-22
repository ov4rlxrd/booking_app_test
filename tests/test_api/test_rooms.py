import pytest



from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


from tests.conftest import auth_header, login_user, create_test_user, create_test_room


@pytest.mark.asyncio
async def test_get_rooms_available(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)


    response = await client.get(
        "/rooms/available",
        params={"booking_date": "2026-06-20"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_room_available_by_id(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    room,slots = await create_test_room(db_session=db_session)

    response = await client.get(
        f"/rooms/available/{room.id}",
        params={"booking_date": "2026-06-20"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["room_id"] == room.id
    assert response.json()["date"] == "2026-06-20"

@pytest.mark.asyncio
async def test_get_room_available_by_nonexistent_id(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)


    response = await client.get(
        "/rooms/available/1",
        params={"booking_date": "2026-06-20"},
        headers=headers
    )
    assert response.status_code == 404