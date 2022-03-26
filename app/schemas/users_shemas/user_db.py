import uuid
from app.schemas.users_shemas import User
from pydantic import Field, UUID4, EmailStr


class UserDB(User):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    login: str = Field(..., max_length=255)
    email: EmailStr
    first_name: str = Field(..., max_length=128)
    last_name: str = Field(..., max_length=128)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    hashed_password: str
