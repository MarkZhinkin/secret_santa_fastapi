from copy import deepcopy
from typing import Generic, Type, Optional, Union

from datetime import datetime
import random

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy import insert, update, select, and_, join
from sqlalchemy.engine import Row

from app.core.db import database

from app.models.bypass_models import Game as GameModel
from app.models.bypass_models import Participant
from app.models.users_models import User as UserModel
from app.schemas.games_schemas import G
from app.schemas.users_schemas import UD


class GameManager(Generic[G]):

    games_db_model: Type[GameModel] = GameModel
    users_db_model: Type[UserModel] = UserModel
    participants_db_model: Type[Participant] = Participant

    # ToDo Remove it later.
    def __init__(self, game_db: Generic[G]):
        self.game_db = game_db

    async def get_current_game(self) -> Union[Row, None]:
        query = select(self.games_db_model).where(
            and_(
                self.games_db_model.game_year == datetime.now().year,
                self.games_db_model.is_registration_open == True,
                self.games_db_model.is_registration_close == False
            )
        )
        return await database.fetch_one(query)

    async def open_game(self):
        query = select(self.games_db_model).where(
            self.games_db_model.game_year == datetime.now().year
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
                query = update(self.games_db_model).where(
                    self.games_db_model.id == result["id"]
                ).values({
                    "is_registration_open": True,
                    "registration_opened_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                await database.execute(query)

    async def add_new_game(self):
        query = insert(self.games_db_model).values({
            "game_year": datetime.utcnow().year,
            "is_registration_open": True,
            "registration_opened_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        await database.fetch_one(query)

    async def close_game(self) -> str:
        query = select(self.games_db_model).where(
            and_(
                self.games_db_model.game_year == datetime.now().year,
                self.games_db_model.is_registration_open == True
            )
        )
        result = await database.fetch_one(query)
        if result is None:
            raise Exception("Game for current year didn't find.")
        else:
            if result["is_registration_close"]:
                raise Exception("Game already close.")
            else:
                query = update(self.games_db_model).where(
                    self.games_db_model.id == result["id"]
                ).values({
                    "is_registration_close": True,
                    "registration_closed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                await database.execute(query)
                return str(result["id"])

    async def generate_pairs(self, game_id: str) -> list:
        query = select(self.users_db_model).where(
            and_(
                self.users_db_model.is_active == True,
                self.users_db_model.is_playing == True,
                self.users_db_model.is_superuser == False
            )
        )
        users = await database.fetch_all(query)
        if len(users) < 2:
            raise Exception("There are too low users in the game.")

        users_dict = self.convert_users_rows_to_dict(users)
        recent_participants_pairs = await self.get_recent_participants_pairs()
        users_dict = self.update_recent_gift_recipients(users_dict, recent_participants_pairs)

        participants_pairs = []
        for user_id, user_value in users_dict.items():
            valid_gift_recipients_dict = self.get_valid_gift_recipients(user_id, users_dict)
            gift_recipient_id = random.choice(list(valid_gift_recipients_dict.keys()))
            users_dict[gift_recipient_id]["is_gift_recipient"] = True

            participants_pair = {
                "secret_santa_id": user_id,
                "gift_recipient_id": gift_recipient_id,
                "preferences": user_value["preferences"]
            }
            participants_pairs.append(participants_pair)
            await self.insert_participants_pair(participants_pair, game_id)

        return participants_pairs

    async def insert_participants_pair(self, participants_pair: dict, game_id: str):
        query = insert(
            self.participants_db_model
        ).values(
            {"game_id": game_id, **participants_pair}
        )
        await database.execute(query)

    async def get_recent_participants_pairs(self, years_before: int = 3) -> list:
        query_join = join(
            self.games_db_model,
            self.participants_db_model,
            self.games_db_model.id == self.participants_db_model.game_id
        )
        query = select(self.participants_db_model).where(
            self.games_db_model.game_year >= datetime.now().year - years_before
        ).select_from(query_join)

        return await database.fetch_all(query)

    @staticmethod
    def get_valid_gift_recipients(user_id: str, users: dict) -> dict:
        return {
            k: v for k, v in users.items() if
            k != user_id and
            k not in users[k]["was_santa_for"] and
            users[k]["is_gift_recipient"] is False
        }

    @staticmethod
    def convert_users_rows_to_dict(users: UD) -> dict:
        return {str(user["id"]): {
            "is_gift_recipient": False,
            "preferences": user["preferences"],
            "was_santa_for": []
        } for user in users}

    def update_recent_gift_recipients(self, users_dict: dict, recent_participants_pairs: list):
        result_dict = deepcopy(users_dict)
        for user_id, user_value in users_dict.items():
            user_participants_pairs = list(filter(lambda x: str(x["secret_santa_id"]) == user_id, recent_participants_pairs))
            result_dict[user_id]["was_santa_for"] = [str(x["gift_recipient_id"]) for x in user_participants_pairs]

        return result_dict


def get_user_db():
    yield SQLAlchemyUserDatabase(GameModel, database, GameModel.__table__)


def get_game_manager(game_db=Depends(get_user_db)):
    yield GameManager(game_db)
