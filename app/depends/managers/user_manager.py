from datetime import datetime, timedelta
from typing import Optional, Union

from pydantic import UUID4

from fastapi import Depends, Request, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users import password
from fastapi_users.manager import BaseUserManager, UserAlreadyExists
from fastapi_users.manager import FastAPIUsersException
# from fastapi_users.password import get_password_hash
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy import select, update, and_, or_, true
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import null



from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from app.core.db import database
from app.core.config import settings

from app.depends.db import get_db

# from app.helpers import SendgridPostOffice
# from app.helpers.template_manager import TemplateManager
from app.helpers.constants import CODE_LIVE_TIME_MINUTES
from app.models.bypass_models.email_verifications import EmailVerification
from app.models.users_models import User as UserModel
from app.schemas.users_shemas import U, UC, UD, UU, UserDB


def get_backend_strategy():
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


jwt_authentication: AuthenticationBackend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl=f'{settings.API_PATH}/auth/jwt/login'),
    get_strategy=get_backend_strategy()
)


class InvalidEmailVerificationCode(FastAPIUsersException):
    pass


class UserNotExists(FastAPIUsersException):
    pass


class UserManager(BaseUserManager[UC, UD]):
    user_db_model = UserDB
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    users_db_model = UserModel
    email_verification_db_model = EmailVerification

    async def validate_password(self, password: str, user: Union[UC, UD]) -> None:
        # ToDo Add validations
        pass

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

    # async def create(
    #         self, user: UC, safe: bool = False, request: Optional[Request] = None, db: Session = Depends(get_db)
    # ) -> user_db_model:
    #
    #     await self.validate_password(user.password, user)
    #
    #     is_email_existing = await self.user_db.get_by_email(user.email)
    #     if is_email_existing is not None:
    #         raise UserAlreadyExists()
    #
    #     email_verification_code = await self.get_last_verification_code("email", user.email, db)
    #     if email_verification_code != user.email_verification_code:
    #         raise InvalidEmailVerificationCode()
    #
    #     hashed_password = get_password_hash(user.password)
    #     user_dict = (
    #         user.create_update_dict() if safe else user.create_update_dict_superuser()
    #     )
    #     db_user = self.user_db_model(**user_dict, hashed_password=hashed_password)
    #
    #     created_user = await self.user_db.create(db_user)
    #
    #     await self.custom_on_after_register(
    #         phone_verification_code=user.phone_verification_code,
    #         email_verification_code=user.email_verification_code
    #     )
    #
    #     return created_user

    # async def custom_on_after_register(
    #         self, phone_verification_code: str, email_verification_code: str
    # ) -> None:
    #     await self.delete_verification_code(param=phone_verification_code, param_name="phone")
    #     await self.delete_verification_code(param=email_verification_code)

    # async def authenticate(
    #         self, credentials: UL, db: Session = Depends(get_db)
    # ) -> user_db_model:
    #
    #     user = await self.get_by_email(credentials.email)
    #
    #     verified, updated_password_hash = password.verify_and_update_password(
    #         credentials.password, user.hashed_password
    #     )
    #     if not verified:
    #         return None
    #
    #     if updated_password_hash is not None:
    #         user.hashed_password = updated_password_hash
    #         await self.user_db.update(user)
    #
    #     return user

    async def get_last_verification_code(self, param_name: str, param: str, db: Session):
        engine_result = db.execute(select(
            [self.email_verification_db_model.code, self.email_verification_db_model.created_at]
        ).where(
            and_(
                self.email_verification_db_model.email == param,
                self.email_verification_db_model.deleted_at == null(),
                self.email_verification_db_model.created_at > datetime.utcnow() - timedelta(minutes=CODE_LIVE_TIME_MINUTES)
            )
        ).order_by(self.email_verification_db_model.id.desc()).limit(1))

        result = engine_result.fetchall()
        if not len(result):
            return None
        return str(result[0]["code"])

    async def get_by_phone(self, phone: str, db: Session) -> UD:
        engine_result = db.execute(select([self.users_db_model.created_at]).where(
            self.users_db_model.phone == phone
        ))
        user = engine_result.fetchall()
        return user if user else None

    async def get_verification_code_by_id(self, param: str, db: Session, param_name: str = "email") -> Optional[UD]:
        engine_result = db.execute(select([self.email_verification_db_model.code, self.email_verification_db_model.email]).where(
            and_(
                self.email_verification_db_model.message_uid == param,
                self.email_verification_db_model.deleted_at == null(),
                self.email_verification_db_model.created_at > datetime.utcnow() - timedelta(minutes=CODE_LIVE_TIME_MINUTES)
            )
        ))

        return engine_result.fetchall()

    async def delete_verification_code(self, param: str, param_name: str = "email"):
        email_query = update(
            self.email_verification_db_model
        ).where(
            self.email_verification_db_model.code == param
        ).values({
            "deleted_at":  datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        })
        await database.execute(email_query)

    # async def user_update_info(self, user_id: UUID4, user_info: UIRQ, db: Session) -> None:
    #     update_query = update(
    #         self.users_db_model
    #     ).where(
    #         self.users_db_model.id == str(user_id)
    #     ).values({
    #         "state": user_info.state,
    #         "city": user_info.city,
    #         "street": user_info.street,
    #         "building": user_info.building,
    #         "postal_code": user_info.postal_code,
    #         "company_name": user_info.company_name,
    #         "has_user_info": True,
    #     })
    #     db.execute(update_query)
    #     db.commit()

    # async def on_after_forgot_password(
    #         self, user: UserModel, token: str, request: Optional[Request] = None
    # ) -> None:
    #     sendgrid = SendgridPostOffice()
    #     href = '/'.join([settings.FRONTEND_DOMAIN, 'reset-password', token])
    #     html_content = TemplateManager.TemplateLetterManager.forgot_password(href)
    #     sendgrid.send_message(
    #         user.email,
    #         html_content
    #     )

    @staticmethod
    def convert_timedelta_to_minutes(timedelta_obj: timedelta) -> float:
        return timedelta_obj.days * 24 * 60 + timedelta_obj.seconds / 60


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

