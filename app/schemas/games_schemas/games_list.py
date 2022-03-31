from typing import List, Union
from app.schemas.games_schemas import Game
from fastapi_users.models import CreateUpdateDictModel


class GameInfo(CreateUpdateDictModel):
    class Config:
        orm_mode = False

    game_year: int
    is_registration_open: bool
    is_registration_close: bool
    participants_pairs: int


class GamesListResponse(Game):
    games_list: List[GameInfo] = []
