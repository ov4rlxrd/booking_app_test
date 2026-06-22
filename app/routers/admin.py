from datetime import date

from fastapi import APIRouter
from starlette import status

from app.core.dependencies import AdminUser
from app.database import SessionDep
from app.service.booking import BookingService

admin_router = APIRouter(prefix="/admin", tags=["admin"])



@admin_router.delete("/booking/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_booking(
    booking_id: int,
    session: SessionDep,
    _: AdminUser
):
    await BookingService.admin_delete_booking(booking_id, session)


@admin_router.get("/bookings", status_code=status.HTTP_200_OK)
async def admin_get_all_bookings(session: SessionDep, _: AdminUser, booking_date: date | None = None):
    return await BookingService.get_all_bookings(session,booking_date)