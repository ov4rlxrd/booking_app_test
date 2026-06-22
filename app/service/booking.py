from datetime import date

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.booking import BookingRepository
from app.repository.room import RoomRepository
from app.schemas.schemas import CreateBooking, BookingResponse, BookingSimpleResponse, RoomSlotActive, \
    RoomAvailabilityResponse
from app.service.room import RoomService


class BookingService:

    @classmethod
    async def create_booking(cls, data: CreateBooking, user_id:int, session: AsyncSession) -> BookingResponse:

        if await BookingRepository.is_booking_exists(data.room_slot_id, data.date, session):
            raise HTTPException(status_code=400, detail="Booking already exists")

        room_for_booking = await RoomService.get_room_by_slot_id(data.room_slot_id, session)
        if not room_for_booking:
            raise HTTPException(status_code=404, detail="Room not found")

        room_slot_for_booking = await RoomRepository.get_room_slot_by_id(data.room_slot_id, session)

        if not room_slot_for_booking:
            raise HTTPException(status_code=404, detail="Room slot not found")

        new_booking = await BookingRepository.create_booking(user_id=user_id, room_slot_id=data.room_slot_id, booking_date=data.date, session=session)



        await session.commit()
        return BookingResponse(id=new_booking.id, room_slot_id=new_booking.room_slot_id, date=new_booking.date, status=new_booking.status, room_name=room_for_booking.name, start_time=room_slot_for_booking.start_time, end_time=room_slot_for_booking.end_time)



    @classmethod
    async def delete_booking(cls, user_id:int ,booking_id:int, session: AsyncSession):
        booking = await BookingRepository.get_booking_by_id(booking_id, session)

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="You can only delete your own bookings")

        await BookingRepository.delete_booking(booking_id, session)
        await session.commit()

    @classmethod
    async def admin_delete_booking(cls, booking_id:int, session: AsyncSession):
        booking = await BookingRepository.get_booking_by_id(booking_id, session)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        await BookingRepository.delete_booking(booking_id, session)
        await session.commit()


    @classmethod
    async def get_bookings(cls, user_id: int, session: AsyncSession) -> list[BookingResponse]:


        bookings = await BookingRepository.get_bookings(user_id=user_id, session=session)

        result = [BookingResponse.model_validate(booking) for booking in bookings]

        return result

    @classmethod
    async def get_all_bookings(cls, session: AsyncSession, booking_date: date | None = None) -> list[BookingResponse]:
        all_bookings = await BookingRepository.get_all_bookings(session=session, booking_date=booking_date)

        result = [BookingResponse.model_validate(booking) for booking in all_bookings]

        return result





