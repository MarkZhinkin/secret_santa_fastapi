from fastapi import APIRouter

from app.api.authorization import auth_router
from app.api.user import user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)

