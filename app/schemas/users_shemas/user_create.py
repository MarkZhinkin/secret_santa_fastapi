from app.schemas.users_shemas import User
from pydantic import Field, EmailStr
from app.helpers.constants import CustomPasswordStr


class UserCreate(User):
    first_name: str = Field(..., max_length=128)
    last_name: str = Field(..., max_length=128)
    email: EmailStr
    login: str = Field(..., max_length=255)
    password: CustomPasswordStr


class UserCreateResponse(User):
    is_active: bool
    access_token: str
    token_type: str
