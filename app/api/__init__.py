from fastapi import APIRouter

from app.api.authorization import auth_router

router = APIRouter(prefix='/authorization')

router.include_router(auth_router)

