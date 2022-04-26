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

    class Config:
        orm_mode = True
        schema_extra = {
            "example": [
                {
                    "game_year": 2019,
                    "is_registration_open": True,
                    "is_registration_close": True,
                    "participants_pairs": 7
                },
                {
                    "game_year": 2020,
                    "is_registration_open": True,
                    "is_registration_close": True,
                    "participants_pairs": 10
                },
                {
                    "game_year": 2021,
                    "is_registration_open": True,
                    "is_registration_close": True,
                    "participants_pairs": 10
                },
                {
                    "game_year": 2022,
                    "is_registration_open": True,
                    "is_registration_close": False,
                    "participants_pairs": 0
                }
            ]
        }
