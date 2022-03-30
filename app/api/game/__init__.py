from fastapi import APIRouter

from . import game_register
from . import open_game
from . import close_game


game_router = APIRouter(prefix='/game')

game_router.include_router(game_register.router)
game_router.include_router(open_game.router)
game_router.include_router(close_game.router)
