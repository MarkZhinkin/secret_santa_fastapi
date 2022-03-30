from .game import Game
from .game_register import GameRegisterResponse, CancelGameRegisterResponse
from .game_open import GameOpenResponse
from .game_close import GameCloseResponse

from typing import TypeVar


G = TypeVar("G", bound=Game)
