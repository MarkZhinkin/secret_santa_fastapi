from fastapi import APIRouter

from . import registration, login


auth_router = APIRouter()

auth_router.include_router(registration.router)
auth_router.include_router(login.router)
