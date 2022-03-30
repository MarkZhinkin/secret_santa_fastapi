from fastapi import APIRouter

from app.api.authorization import auth_router
from app.api.user import user_router
from app.api.game import game_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(game_router)

