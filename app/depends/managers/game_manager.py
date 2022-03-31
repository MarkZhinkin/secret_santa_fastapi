from copy import deepcopy
from typing import Generic, Type, Union

from datetime import datetime
import random

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy import insert, update, select, and_, join, func
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

        for user in users:
            await self.change_user_game_status(user)

        if len(users) < 2:
            raise Exception("There are too low users in the game.")

        users_dict = self.convert_users_rows_to_dict(users)
        recent_participants_pairs = await self.get_recent_participants_pairs()
        users_dict = self.update_recent_gift_recipients(users_dict, recent_participants_pairs)

        participants_pairs = []
        for user_id, user_value in users_dict.items():
            valid_gift_recipients_dict = self.get_valid_gift_recipients(user_id, users_dict)
            if len(list(valid_gift_recipients_dict.keys())) != 0:
                gift_recipient_id = random.choice(list(valid_gift_recipients_dict.keys()))
                users_dict[gift_recipient_id]["is_gift_recipient"] = True
            else:
                gift_recipient_id = None

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

    async def get_games_list(self) -> list:
        query_join = join(
            self.games_db_model,
            self.participants_db_model,
            self.games_db_model.id == self.participants_db_model.game_id
        )
        query = select(
            self.games_db_model,
            func.count(self.participants_db_model.id).label("participants_pairs")
        ).select_from(
            query_join
        ).group_by(self.participants_db_model.game_id)
        games = await database.fetch_all(query)
        return [
            {
                "game_year": game["game_year"],
                "is_registration_open": game["is_registration_open"],
                "is_registration_close": game["is_registration_close"],
                "participants_pairs": game["participants_pairs"],
            }
            for game in games
        ]

    async def get_participants_pairs(self, selected_year: int) -> list:
        query_join = join(
            self.games_db_model,
            self.participants_db_model,
            self.games_db_model.id == self.participants_db_model.game_id
        )
        query = select(
            self.participants_db_model
        ).select_from(
            query_join
        ).where(
            self.games_db_model.game_year == selected_year
        )
        participants_pairs = await database.fetch_all(query)

        query = select(
            self.users_db_model
        ).where(
            self.users_db_model.is_verified == True
        )
        users = await database.fetch_all(query)
        users_dict = {
            user["id"]: {
                "first_name": user["first_name"],
                "last_name": user["last_name"]
            }
            for user in users
        }
        return [
            {
                "secret_santa_full_name": " ".join((
                    users_dict[participants_pair["secret_santa_id"]]["first_name"],
                    users_dict[participants_pair["secret_santa_id"]]["last_name"]
                )),
                "gift_recipient_full_name":  " ".join((
                    users_dict[participants_pair["gift_recipient_id"]]["first_name"],
                    users_dict[participants_pair["gift_recipient_id"]]["last_name"]
                )),
                "preferences": participants_pair["preferences"]
            }
            for participants_pair in participants_pairs
        ]

    async def change_user_game_status(self, user: UD):
        query = update(
            self.users_db_model
        ).values({
            "is_playing": False
        }).where(
            self.users_db_model.id == user.id
        )

        await database.execute(query)

    async def get_gift_recipient_info(self, user: UD) -> Union[Row, None]:
        query_join = join(
            self.participants_db_model,
            self.games_db_model,
            self.participants_db_model.game_id == self.games_db_model.id
        ).join(
            self.users_db_model,
            self.participants_db_model.gift_recipient_id == self.users_db_model.id
        )

        query = select(
            self.users_db_model.first_name,
            self.users_db_model.last_name,
            self.users_db_model.department,
            self.users_db_model.city,
            self.users_db_model.street,
            self.users_db_model.building,
            self.participants_db_model.preferences
        ).where(
            self.participants_db_model.secret_santa_id == user.id
        ).select_from(
            query_join
        )

        return await database.fetch_one(query)

    @staticmethod
    def get_valid_gift_recipients(user_id: str, users: dict) -> dict:
        return {
            k: v
            for k, v in users.items() if
            k != user_id and
            k not in users[user_id]["was_santa_for"] and
            v["is_gift_recipient"] is False
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
