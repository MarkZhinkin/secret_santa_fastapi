from datetime import datetime, timedelta
from typing import Union, Type

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.manager import BaseUserManager
from fastapi_users.manager import FastAPIUsersException
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy import insert, select, update, and_, or_, true
from sqlalchemy.sql import null
from sqlalchemy.engine import Row

from app.core.db import database
from app.core.config import settings

from app.helpers.constants import CODE_LIVE_TIME_MINUTES
from app.models.bypass_models.email_verifications import EmailVerification
from app.models.users_models import User as UserModel
from app.schemas.users_schemas import U, UC, UD, UU, UserDB
from app.schemas.emails_schemas import EVCCRQ

from app.depends.swagger_support_jwt_authentication import SwaggerSupportJWTAuthentication


jwt_authentication: SwaggerSupportJWTAuthentication = SwaggerSupportJWTAuthentication(
    secret=settings.SECRET_KEY,
    lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    tokenUrl=f'{settings.API_PATH}/auth/jwt/login',
)


class InvalidEmailVerificationCode(FastAPIUsersException):
    pass


class UserNotExists(FastAPIUsersException):
    pass


class UserManager(BaseUserManager[UC, UD]):
    user_db_model: Type[UD] = UserDB
    reset_password_token_secret: str = settings.SECRET_KEY
    verification_token_secret: str = settings.SECRET_KEY

    users_db_model: Type[UserModel] = UserModel
    email_verification_db_model: Type[EmailVerification] = EmailVerification

    async def get_by_email(self, login_or_email: str) -> UD:
        query = select(
            self.users_db_model
        ).where(
            and_(
                or_(
                    self.users_db_model.login == login_or_email,
                    self.users_db_model.email == login_or_email,
                ),
                self.users_db_model.is_active == true()
            )

        )
        user = await database.fetch_one(query)

        if user is None:
            raise UserNotExists()

        return user

    async def add_verification_code(self, email: str, code: str, message_uid: str) -> Union[bool, None]:
        query = insert(self.email_verification_db_model).values({
            "email": email,
            "code": code,
            "message_uid": message_uid
        })
        return await database.execute(query)

    async def get_verification_code_by_id(self, verification_code_item: EVCCRQ) -> Union[Row, None]:
        query = select([self.email_verification_db_model.code, self.email_verification_db_model.email]).where(
            and_(
                self.email_verification_db_model.message_uid == verification_code_item.message_uid,
                self.email_verification_db_model.code == verification_code_item.code,
                self.email_verification_db_model.deleted_at == null(),
                self.email_verification_db_model.created_at > datetime.utcnow() - timedelta(
                    minutes=CODE_LIVE_TIME_MINUTES)
            )
        )
        return await database.fetch_one(query)

    async def delete_verification_code(self,message_uid: str):
        query = update(
            self.email_verification_db_model
        ).where(
            self.email_verification_db_model.message_uid == message_uid
        ).values({
            "deleted_at":  datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        })

        await database.execute(query)

    async def change_user_right(self, user: UD):
        change_user_right_query = update(
            self.users_db_model
        ).where(
            self.users_db_model.id == user.id
        ).values({
            "is_verified": True
        })

        await database.execute(change_user_right_query)

        check_user_right_query = select(
            self.users_db_model.is_verified
        ).where(
            and_(
                self.users_db_model.id == user.id,
                self.users_db_model.is_verified == True
            )
        )
        verified_user = await database.fetch_one(check_user_right_query)
        if verified_user is None:
            raise Exception("Users right didn't change.")

    async def get_user_info(self,user: UD) -> UD:
        query = select(
            self.users_db_model.preferences,
            self.users_db_model.department,
            self.users_db_model.city,
            self.users_db_model.street,
            self.users_db_model.building,
        ).where(
            self.users_db_model.id == user.id
        )
        return await database.fetch_one(query)

    async def change_user_info(self, user: UD, user_info_item: dict):
        query = update(
            self.users_db_model
        ).where(
            self.users_db_model.id == user.id
        ).values(
            user_info_item
        )

        await database.execute(query)

    async def get_playing_users(self) -> list:
        query = select(
            self.users_db_model.first_name,
            self.users_db_model.last_name,
            self.users_db_model.email,
            self.users_db_model.department
        ).where(
            self.users_db_model.is_playing == True
        )

        playing_users = await database.fetch_all(query)
        return [
            {
                "first_name": playing_user["first_name"],
                "last_name": playing_user["last_name"],
                "email": playing_user["email"],
                "department": playing_user["department"],
            }
            for playing_user in playing_users
        ]

    @staticmethod
    def convert_timedelta_to_minutes(timedelta_obj: timedelta) -> float:
        return timedelta_obj.days * 24 * 60 + timedelta_obj.seconds / 60

    @staticmethod
    def validate_login_and_password(login, password):
        LOGIN_ERROR_MESSAGE = "login must have length between 4 and 15 symbols, dont include special symbols and spaces."
        PASSWORD_ERROR_MESSAGE = "password must have length more than 8 symbols, include upper and lower letters and special symbols."

        if len(login) < 4 or len(login) > 15:
            raise Exception(LOGIN_ERROR_MESSAGE)
        if list(filter(lambda x: x != "_" and not x.isalpha() and not x.isdigit(), login)):
            raise Exception(LOGIN_ERROR_MESSAGE)

        lower_symbols_list = [chr(x) for x in range(97, 123)]
        upper_symbols_list = [chr(x) for x in range(65, 91)]
        special_symbols_list = \
            [chr(x) for x in range(32, 65)] + \
            [chr(x) for x in range(91, 95)] + \
            [chr(x) for x in range(123, 127)]

        if len(password) < 8:
            raise Exception(PASSWORD_ERROR_MESSAGE)
        if not list(filter(lambda x: x in lower_symbols_list, password)):
            raise Exception(PASSWORD_ERROR_MESSAGE)
        if not list(filter(lambda x: x in upper_symbols_list, password)):
            raise Exception(PASSWORD_ERROR_MESSAGE)
        if not list(filter(lambda x: x in special_symbols_list, password)):
            raise Exception(PASSWORD_ERROR_MESSAGE)


def get_user_db():
    yield SQLAlchemyUserDatabase(UserModel, database, UserModel.__table__)


def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_authentication],
    U,
    UC,
    UU,
    UD,
)

blocked_user = fastapi_users.current_user(active=False, verified=False, superuser=False)
unverified_user = fastapi_users.current_user(active=True, verified=False, superuser=False)
verified_user = fastapi_users.current_user(active=True, verified=True, superuser=False)
admin_user = fastapi_users.current_user(active=True, verified=True, superuser=True)

