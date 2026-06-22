from contextlib import asynccontextmanager

from fastapi import FastAPI



from app.database import engine
from app.routers.admin import admin_router
from app.routers.bookings import booking_router
from app.routers.rooms import room_router
from app.routers.user import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(users_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(admin_router)