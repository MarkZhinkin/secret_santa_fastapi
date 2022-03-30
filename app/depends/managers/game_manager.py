from typing import Generic, Type, Optional

from datetime import datetime
from typing import Union

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy import insert, update, select, and_
from sqlalchemy.engine import Row

from app.core.db import database

from app.models.bypass_models import Game as GameModel
from app.schemas.games_schemas import G


class GameManager(Generic[G]):

    games_gb_model: Type[GameModel] = GameModel

    # ToDo Remove it later.
    def __init__(self, game_db: Generic[G]):
        self.game_db = game_db

    async def get_current_game(self) -> Union[Row, None]:
        query = select(self.games_gb_model).where(
            and_(
                self.games_gb_model.game_year == datetime.now().year,
                self.games_gb_model.is_registration_open == True,
                self.games_gb_model.is_registration_close == False
            )
        )
        return await database.fetch_one(query)

    async def open_game(self):
        query = select(self.games_gb_model).where(
            self.games_gb_model.game_year == datetime.now().year
        )
        result = await database.fetch_one(query)
        if result is None:
            await self.add_new_game()
        else:
            if result["is_registration_open"] and not result["is_registration_close"]:
                raise Exception("Game already open.")
            elif result["is_registration_close"]:
                raise Exception("Game already close.")
            else:
                query = update(self.games_gb_model).where(
                    self.games_gb_model.id == result["id"]
                ).values({
                    "is_registration_open": True,
                    "registration_opened_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                await database.execute(query)

    async def add_new_game(self):
        query = insert(self.games_gb_model).values({
            "game_year": datetime.utcnow().year,
            "is_registration_open": True,
            "registration_opened_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        await database.fetch_one(query)

    async def close_game(self):
        query = select(self.games_gb_model).where(
            self.games_gb_model.game_year == datetime.now().year
        )
        result = await database.fetch_one(query)
        if result is None:
            raise Exception("Game for current year didn't find.")
        else:
            if result["is_registration_close"]:
                raise Exception("Game already close.")
            else:
                query = update(self.games_gb_model).where(
                    self.games_gb_model.id == result["id"]
                ).values({
                    "is_registration_close": True,
                    "registration_closed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                await database.execute(query)


def get_user_db():
    yield SQLAlchemyUserDatabase(GameModel, database, GameModel.__table__)


def get_game_manager(game_db=Depends(get_user_db)):
    yield GameManager(game_db)
