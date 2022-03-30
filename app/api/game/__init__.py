from fastapi import APIRouter

from . import game_register


game_router = APIRouter(prefix='/game')

game_router.include_router(game_register.router)
