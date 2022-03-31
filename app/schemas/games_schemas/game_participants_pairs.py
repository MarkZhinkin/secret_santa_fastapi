from typing import List, Union
from app.schemas.games_schemas import Game
from fastapi_users.models import CreateUpdateDictModel


class ParticipantsPairs(CreateUpdateDictModel):
    class Config:
        orm_mode = False

    secret_santa_full_name: str
    gift_recipient_full_name: str
    preferences: Union[str, None]


class GameParticipantsPairsResponse(Game):
    playing_users_list: List[ParticipantsPairs] = []


class GameParticipantsPairsRequest(Game):
    year: int
