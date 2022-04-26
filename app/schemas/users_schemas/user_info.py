from app.schemas.users_schemas import User
from typing import Union, Optional


class UserInfoResponse(User):
    preferences: Union[str, None] = None
    department: Union[str, None] = None
    city: Union[str, None] = None
    street: Union[str, None] = None
    building: Union[str, None] = None

    class Config:
        schema_extra = {
            "example": {
                "preferences": "A good book.",
                "department": "Editorial department",
                "city": "New York",
                "street": "West 10th Street",
                "building": "14"
            }
        }


class UserInfoChangeRequest(User):
    preferences: Optional[str]
    department: Optional[str]
    city: Optional[str]
    street: Optional[str]
    building: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "preferences": "A good book.",
                "department": "Editorial department",
                "city": "New York",
                "street": "West 10th Street",
                "building": "14"
            }
        }


class UserInfoChangeResponse(User):
    is_info_change: bool = False

    class Config:
        schema_extra = {
            "example": {
                "is_info_change": True
            }
        }
