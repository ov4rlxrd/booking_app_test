import sys
from datetime import time
from typing import AsyncGenerator

import pytest
import os

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from app.database import Model, get_db
from app.models.booking import Room, RoomSlot
from main import app


from app.database import Model

os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5436/test_booking_db"
os.environ["SECRET_KEY"] = ("test_secret_key_for_testing_only")


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(
        os.environ["DATABASE_URL"],poolclass=NullPool
    )
    return engine

@pytest.fixture(scope="session")
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
async def db_session(
        test_engine,
        setup_database,
) -> AsyncGenerator[AsyncSession]:
    conn = await test_engine.connect()
    trans = await conn.begin()

    test_async_session = async_sessionmaker(
        bind=conn, expire_on_commit=False, class_=AsyncSession, join_transaction_mode="create_savepoint"
    )

    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()

@pytest.fixture
async def client(
        db_session: AsyncSession
)-> AsyncGenerator[AsyncClient]:
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


async def create_test_user(
        client:AsyncClient,
        login:str = "login",
        password:str = "testpassword123"

) -> dict:
    response = await client.post(
        "/users",
        json={"login": login, "password": password}
    )
    assert response.status_code == 201, f"Failed to create user: {response.text}"
    return response.json()

async def login_user(
        client:AsyncClient,
        login :str="login",
        password:str="testpassword123"
) ->str:
    response = await client.post(
        "/users/token",
        data={"username": login, "password": password}
    )
    assert response.status_code == 200, f"Failed to login user: {response.text}"
    return response.json()["access_token"]

def auth_header(token:str)->dict[str, str]:
    return {"Authorization": f"Bearer {token}"}

async def create_test_room(
        db_session: AsyncSession,
        name: str = "Переговорная Тест") -> tuple[Room, list[RoomSlot]]:
    room = Room(name=name, description= "Тест")
    db_session.add(room)
    await db_session.flush()

    slots = [
        RoomSlot(room_id=room.id, start_time=time(10, 0), end_time=time(12, 0)),
        RoomSlot(room_id=room.id, start_time=time(13, 0), end_time=time(16, 0))
    ]

    db_session.add_all(slots)
    await db_session.flush()
    await db_session.commit()

    return room, slots


