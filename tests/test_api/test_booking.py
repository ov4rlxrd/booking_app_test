import pytest



from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


from tests.conftest import auth_header, login_user, create_test_user, create_test_room



@pytest.mark.asyncio
async def test_create_booking(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    room, slots = await create_test_room(db_session=db_session)

    response = await client.post(
        "/booking",
        json={
            "room_slot_id": slots[0].id,
            "date": "2026-06-20"
        },
        headers=headers
    )

    assert response.status_code == 201
    assert response.json()["room_slot_id"] == slots[0].id
    assert response.json()["date"] == "2026-06-20"
    assert response.json()["status"] == "active"


@pytest.mark.asyncio
async def test_create_booking_with_non_existing_slot(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    room, slots = await create_test_room(db_session=db_session)

    response = await client.post(
        "/booking",
        json={
            "room_slot_id": 999,
            "date": "2026-06-20"
        },
        headers=headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_booking_with_existing_booking(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    room, slots = await create_test_room(db_session=db_session)

    await client.post(
        "/booking",
        json={
            "room_slot_id": slots[0].id,
            "date": "2026-06-20"
        },
        headers=headers
    )

    response = await client.post(
        "/booking",
        json={
            "room_slot_id": slots[0].id,
            "date": "2026-06-20"
        },
        headers=headers
    )

    assert response.status_code == 400

async def test_delete_booking(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    room, slots = await create_test_room(db_session=db_session)

    booking_response = await client.post(
        "/booking",
        json={
            "room_slot_id": slots[0].id,
            "date": "2026-06-20"
        },
        headers=headers
    )

    response = await client.delete(
        f"/booking/{booking_response.json()['id']}",
        headers=headers
    )

    assert response.status_code == 204



async def test_delete_nonexisting_booking(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    await create_test_room(db_session=db_session)


    response = await client.delete(
        "/booking/999",
        headers=headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_other_booking(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token1 = await login_user(client)
    headers1 = auth_header(token1)

    room, slots = await create_test_room(db_session)

    booking = await client.post(
        "/booking",
        json={"room_slot_id":slots[0].id, "date":"2026-06-20"},
        headers=headers1,
    )

    await create_test_user(client, login="test_user2")
    token2 = await login_user(client, login="test_user2")
    headers2 = auth_header(token2)

    response = await client.delete(
        f"/booking/{booking.json()['id']}",
        headers=headers2,
    )


    assert response.status_code == 403


async def test_get_bookings(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token = await login_user(client)
    headers = auth_header(token)

    room, slots = await create_test_room(db_session=db_session)

    await client.post(
        "/booking",
        json={
            "room_slot_id": slots[0].id,
            "date": "2026-06-20"
        },
        headers=headers
    )

    response = await client.get(
        "/booking/my",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_user_without_access_token(client: AsyncClient):
    response = await client.get(
        "/booking/my"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_other_user_bookings(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(client)
    token1 = await login_user(client)
    headers1 = auth_header(token1)

    room, slots = await create_test_room(db_session)

    await client.post(
        "/booking",
        json={"room_slot_id":slots[0].id, "date":"2026-06-20"},
        headers=headers1,
    )

    await create_test_user(client, login="test_user2")
    token2 = await login_user(client, login="test_user2")
    headers2 = auth_header(token2)

    response = await client.get(
        f"/booking/my",
        headers=headers2,
    )


    assert response.json() == []