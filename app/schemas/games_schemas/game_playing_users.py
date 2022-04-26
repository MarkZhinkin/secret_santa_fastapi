from typing import List, Union
from pydantic import Field, EmailStr
from app.schemas.games_schemas import Game
from fastapi_users.models import CreateUpdateDictModel


class GamePlayingUser(CreateUpdateDictModel):
    class Config:
        orm_mode = False

    first_name: str = Field(..., max_length=128)
    last_name: str = Field(..., max_length=128)
    email: EmailStr
    department: Union[str, None] = None


class GamePlayingUsersResponse(Game):
    playing_users_list: List[GamePlayingUser] = []

    class Config:
        schema_extra = {
            "example": [
                {
                    "first_name": "Stephen",
                    "last_name": "King",
                    "email": "horror.king@stephenking.com"
                },
                {
                    "first_name": "George",
                    "last_name": "Martin",
                    "email": "king.of.night.king@georgerrmartin.com"
                },
                {
                    "first_name": "Joanne",
                    "last_name": "Rowling",
                    "email": "witchcraft.queen.king@jkrowling.com"
                },
            ]
        }
