from app.schemas.games_schemas import Game
from typing import Union


class BaseGameRegister(Game):
    reason: Union[str, None] = None


class GameRegisterResponse(BaseGameRegister):
    is_register_to_game: bool = False


class CancelGameRegisterResponse(BaseGameRegister):
    is_cancel_register_to_game: bool = False
