from fastapi import APIRouter
from starlette import status

from app.core.dependencies import CurrentUser
from app.database import SessionDep
from app.schemas.schemas import BookingResponse, CreateBooking
from app.service.booking import BookingService

booking_router = APIRouter(prefix="/booking", tags=["booking"])



@booking_router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(booking: CreateBooking,current_user:CurrentUser, session: SessionDep) -> BookingResponse:
    new_booking = await BookingService.create_booking(booking,current_user.id,  session)
    return new_booking


@booking_router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id:int, current_user:CurrentUser, session: SessionDep):
    await BookingService.delete_booking(current_user.id, booking_id,session)

@booking_router.get("/my", status_code=status.HTTP_200_OK)
async def get_bookings(current_user:CurrentUser,session: SessionDep) -> list[BookingResponse]:
    bookings = await BookingService.get_bookings(current_user.id,session)

    return bookings




