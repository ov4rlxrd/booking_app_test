import asyncio
import selectors
import sys
from datetime import time

from app.core.security import hash_password
from app.database import new_session
from app.models.booking import Room, RoomSlot, User


async def seed():
    async with new_session() as session:
        rooms = [
            Room(name="Переговорная А", description="Проектор, whiteboard, 8 мест"),
            Room(name="Переговорная Б", description="ТВ-панель, 4 места"),
            Room(name="Переговорная В", description="Без оборудования, 6 мест"),
        ]
        session.add_all(rooms)
        await session.flush()

        slots = [
            RoomSlot(room_id=rooms[0].id, start_time=time(9, 0), end_time=time(11, 0)),
            RoomSlot(room_id=rooms[0].id, start_time=time(11, 0), end_time=time(13, 0)),
            RoomSlot(room_id=rooms[0].id, start_time=time(13, 0), end_time=time(16, 0)),
            RoomSlot(room_id=rooms[0].id, start_time=time(16, 0), end_time=time(18, 0)),
            RoomSlot(room_id=rooms[1].id, start_time=time(9, 0), end_time=time(12, 0)),
            RoomSlot(room_id=rooms[1].id, start_time=time(13, 0), end_time=time(17, 0)),
            RoomSlot(room_id=rooms[2].id, start_time=time(10, 0), end_time=time(12, 0)),
            RoomSlot(room_id=rooms[2].id, start_time=time(14, 0), end_time=time(16, 0)),
            RoomSlot(room_id=rooms[2].id, start_time=time(16, 0), end_time=time(18, 0)),
        ]
        users = [
            User(login="admin", password_hash=hash_password("admin123"), role="admin"),
            User(login="employee", password_hash=hash_password("emp123"), role="employee"),
        ]


        session.add_all(users)


        session.add_all(slots)
        await session.commit()


if __name__ == "__main__":
    if sys.platform == "win32":
        loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
        asyncio.run(seed(), loop_factory=lambda: loop)
    else:
        asyncio.run(seed())