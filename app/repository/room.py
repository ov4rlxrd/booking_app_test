from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Room, RoomSlot


class RoomRepository:
    @classmethod
    async def get_rooms(cls, session: AsyncSession):
        query = select(Room)
        result = await session.execute(query)

        return list(result.scalars().all())


    @classmethod
    async def get_room_slot_by_id(cls, slot_id: int, session:AsyncSession) -> RoomSlot | None:
         return await session.scalar(select(RoomSlot).where(RoomSlot.id == slot_id))

    @classmethod
    async def get_room_by_id(cls, room_id: int, session:AsyncSession) -> Room | None:
        return await session.scalar(select(Room).where(Room.id == room_id))


