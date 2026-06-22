from datetime import date
from typing import List

from fastapi import APIRouter
from starlette import status

from app.core.dependencies import CurrentUser
from app.database import SessionDep
from app.schemas.schemas import RoomResponse, RoomAvailabilityResponse
from app.service.room import RoomService

room_router = APIRouter(prefix="/rooms", tags=["rooms"])


@room_router.get("", status_code=status.HTTP_200_OK)
async def get_rooms(session: SessionDep, current_user: CurrentUser)->List[RoomResponse]:
    rooms = await RoomService.get_rooms(session)

    return rooms

@room_router.get("/available", status_code=status.HTTP_200_OK)
async def get_available_rooms(booking_date:date, session: SessionDep, current_user: CurrentUser)->list[RoomAvailabilityResponse]:
    return await RoomService.get_room_available_for_booking(booking_date, session)

@room_router.get("/available/{room_id}", status_code=status.HTTP_200_OK)
async def get_availability_for_room(room_id:int, booking_date:date, session: SessionDep, current_user: CurrentUser):
    active_bookings = await RoomService.get_active_bookings(room_id,booking_date,session)

    return active_bookings


@room_router.get("/{room_id}", status_code=status.HTTP_200_OK)
async def get_room(room_id:int,session: SessionDep, current_user: CurrentUser)->RoomResponse:
    room = await RoomService.get_room_by_id(room_id, session)

    return room