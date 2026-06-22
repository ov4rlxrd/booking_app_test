from datetime import date
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, Room, RoomSlot


class BookingRepository:

    @classmethod
    async def create_booking(cls, user_id: int, room_slot_id:int , booking_date: date, session: AsyncSession) -> Booking:

        booking = Booking(user_id=user_id, room_slot_id=room_slot_id, date=booking_date, status="active")

        session.add(booking)
        await session.flush()
        return booking

    @classmethod
    async def delete_booking(cls, booking_id:int, session: AsyncSession):
        booking = await BookingRepository.get_booking_by_id(booking_id, session)

        if booking is None:
            return None

        booking.status = "inactive"
        await session.flush()
        await session.refresh(booking)
        return True

    @classmethod
    async def get_bookings(cls, user_id: int, session: AsyncSession):
        query = (
            select(
                Booking.id,
                Booking.room_slot_id,
                Booking.date,
                Booking.status,
                Room.name.label("room_name"),
                RoomSlot.start_time,
                RoomSlot.end_time,
            )
            .join(RoomSlot, Booking.room_slot_id == RoomSlot.id)
            .join(Room, RoomSlot.room_id == Room.id)
            .where(Booking.user_id == user_id)
        )

        result = await session.execute(query)


        return result.mappings().all()

    @classmethod
    async def get_all_bookings(cls, session: AsyncSession, booking_date: date | None = None):
        query = (
            select(
                Booking.id,
                Booking.room_slot_id,
                Booking.date,
                Booking.status,
                Room.name.label("room_name"),
                RoomSlot.start_time,
                RoomSlot.end_time,
            )
            .join(RoomSlot, Booking.room_slot_id == RoomSlot.id)
            .join(Room, RoomSlot.room_id == Room.id)
        )

        if booking_date is not None:
            query = query.where(Booking.date == booking_date)

        result = await session.execute(query)

        return result.mappings().all()


    @classmethod
    async def get_booking_by_id(
            cls, booking_id:int, session: AsyncSession
    ) -> Booking | None:
        return await session.scalar(select(Booking)
                                    .where(
            Booking.id == booking_id,
        )
    )



    @classmethod
    async def get_active_bookings_for_slot(cls, room_slot_id: int,booking_date:date,  session: AsyncSession) -> Booking | None:
        query = (
            select(Booking)
            .join(RoomSlot, Booking.room_slot_id == RoomSlot.id)
            .where(
                Booking.room_slot_id == room_slot_id,
                Booking.date == booking_date,
                Booking.status == "active",
            )
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def is_booking_exists(cls, room_slot_id:int, booking_date:date,  session: AsyncSession) -> bool:
        booking = await session.scalar(select(Booking)
                                    .where(
            Booking.room_slot_id == room_slot_id,
            Booking.date == booking_date,
            )
        )
        return booking is not None

