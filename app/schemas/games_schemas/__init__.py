from .game import Game
from .game_register import GameRegisterResponse, CancelGameRegisterResponse

from typing import TypeVar


G = TypeVar("G", bound=Game)
