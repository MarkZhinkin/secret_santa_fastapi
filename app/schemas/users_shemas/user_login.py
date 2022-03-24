from typing import Union
from app.schemas.users_shemas import User
from pydantic import Field, EmailStr
from app.helpers.constants import CustomPasswordStr


class UserLogin(User):
    login_or_email: Union[EmailStr, str] = Field(..., max_length=255)
    password: CustomPasswordStr


class UserLoginResponse(User):
    access_token: str
    token_type: str
