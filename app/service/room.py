from datetime import date

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.booking import BookingRepository
from app.repository.room import RoomRepository
from app.schemas.schemas import RoomResponse, RoomAvailabilityResponse, RoomSlotActive


class RoomService:

    @classmethod
    async def get_rooms(cls, session):

        rooms = await RoomRepository.get_rooms(session)

        result = [RoomResponse.model_validate(room) for room in rooms]

        return result


    @classmethod
    async def get_room_by_slot_id(cls, slot_id: int, session):

        room_slot = await RoomRepository.get_room_slot_by_id(slot_id, session)

        if not room_slot:
            raise HTTPException(status_code=404, detail="Room slot not found")

        room = await RoomRepository.get_room_by_id(room_slot.room_id, session)

        result = RoomResponse.model_validate(room)

        return result


    @classmethod
    async def get_room_by_id(cls, room_id: int, session):

        room = await RoomRepository.get_room_by_id(room_id, session)

        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        result = RoomResponse.model_validate(room)

        return result

    @classmethod
    async def get_active_bookings(cls, room_id: int, booking_date: date,
                                  session: AsyncSession) -> RoomAvailabilityResponse:
        room = await RoomRepository.get_room_by_id(room_id, session)

        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        room_slots = []

        for slot in room.slots:
            booking = await BookingRepository.get_active_bookings_for_slot(slot.id, booking_date, session)

            room_slots.append(RoomSlotActive(slot_id=slot.id, start_time=slot.start_time, end_time=slot.end_time,
                                             is_available=booking is None))

        return RoomAvailabilityResponse(room_id=room.id, room_name=room.name, date=booking_date, slots=room_slots)


    @classmethod
    async def get_room_available_for_booking(cls, booking_date: date, session: AsyncSession) -> list[RoomAvailabilityResponse]:

        rooms = await RoomRepository.get_rooms(session)

        room_slots = []

        for room in rooms:

            available_for_booking = await cls.get_active_bookings(room.id, booking_date, session)
            room_slots.append(available_for_booking)
        return room_slots
