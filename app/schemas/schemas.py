from datetime import time, date
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr


class UserBase(BaseModel):
    id: int
    login: str
    role: str


class UserResponse(BaseModel):
    login: str
    role: str

class UserCreate(BaseModel):
    login: str
    password: str



class RoomResponse(BaseModel):
    id: int
    name: str
    description: str

    slots: list["RoomSlotResponse"]

    model_config = ConfigDict(from_attributes=True)

class RoomAvailabilityResponse(BaseModel):
    room_id: int
    room_name: str
    date: date
    slots: list["RoomSlotActive"]


class RoomSlotResponse(BaseModel):
    id: int
    room_id: int
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)

class RoomSlotActive(BaseModel):
    slot_id: int
    start_time: time
    end_time: time
    is_available: bool
    model_config = ConfigDict(from_attributes=True)



class CreateBooking(BaseModel):
    room_slot_id: int
    date: date

class BookingResponse(BaseModel):
    id:int
    room_slot_id: int
    date: date
    status:str
    room_name: str
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)


class BookingSimpleResponse(BaseModel):
    id: int
    user_id: int
    room_slot_id: int
    date: date
    status: str

    model_config = ConfigDict(from_attributes=True)



class Token(BaseModel):
    access_token: str
    token_type: str