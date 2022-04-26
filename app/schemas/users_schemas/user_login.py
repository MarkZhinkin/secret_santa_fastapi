from typing import Union
from app.schemas.users_schemas import User
from pydantic import Field, EmailStr
from app.helpers.constants import CustomPasswordStr


class UserLogin(User):
    username: Union[EmailStr, str] = Field(..., max_length=255)
    password: CustomPasswordStr

    class Config:
        schema_extra = {
            "example": {
                "username": "Mark_Twain or clemens.samuel@gmail.com",
                "password": ">w^uTPUb5-Jj"
            }
        }


class UserLoginResponse(User):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
                                "eyJ1c2VyX2lkIjoiNWM3OGMyOTktMDc3ZC00Y"
                                "jBiLWJlNjctYjk3YzdjMjVhM2YzIiwiYXVkIj"
                                "pbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAi"
                                "OjE2NDkwNjA5Mjh9.N7dwXIb4z6IY1pZX1Wh8O"
                                "HH27c5A1J1VijOA7UI9Gvk",
                "token_type": "bearer"
            }
        }
