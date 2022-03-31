from .user import User
from .user_create import UserCreate, UserCreateResponse
from .user_login import UserLogin, UserLoginResponse
from .user_update import UserUpdate
from .user_db import UserDB
from .user_info import (
    UserInfoResponse,
    UserInfoChangeRequest,
    UserInfoChangeResponse
)
from .gift_recipient_info import GiftRecipientInfoResponse

from typing import TypeVar


U = TypeVar("U", bound=User)
UC = TypeVar("UC", bound=UserCreate)
UU = TypeVar("UU", bound=UserUpdate)
UD = TypeVar("UD", bound=UserDB)
