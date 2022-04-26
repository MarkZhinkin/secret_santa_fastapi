from app.schemas.users_schemas import User
from pydantic import Field, EmailStr
from app.helpers.constants import CustomPasswordStr


class UserCreate(User):
    first_name: str = Field(..., max_length=128)
    last_name: str = Field(..., max_length=128)
    email: EmailStr
    login: str = Field(..., max_length=255)
    password: CustomPasswordStr

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Samuel",
                "last_name": "Clemens",
                "email": "clemens.samuel@gmail.com",
                "login": "Mark_Twain",
                "password": ">w^uTPUb5-Jj"
            }
        }


class UserCreateResponse(User):
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
