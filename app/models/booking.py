from datetime import datetime, date


from sqlalchemy import ForeignKey, DateTime, Time, Date

from app.database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship



class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)


class Room(Model):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    slots: Mapped[list["RoomSlot"]] = relationship(back_populates="room", cascade="all, delete, delete-orphan", lazy="selectin")



class RoomSlot(Model):
    __tablename__ = "room_slots"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)

    room: Mapped[Room] = relationship(back_populates="slots", lazy="selectin")


class Booking(Model):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_slot_id: Mapped[int] = mapped_column(ForeignKey("room_slots.id"))
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

