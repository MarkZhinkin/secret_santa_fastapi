from app.schemas.users_shemas import User
from typing import Union, Optional


class UserInfoResponse(User):
    preferences: Union[str, None] = None
    department: Union[str, None] = None
    city: Union[str, None] = None
    street: Union[str, None] = None
    building: Union[str, None] = None


class UserInfoChangeRequest(User):
    preferences: Optional[str]
    department: Optional[str]
    city: Optional[str]
    street: Optional[str]
    building: Optional[str]


class UserInfoChangeResponse(User):
    is_info_change: bool = False
