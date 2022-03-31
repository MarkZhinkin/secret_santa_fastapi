from typing import Optional, Union
from app.schemas.users_schemas import User


class GiftRecipientInfoResponse(User):
    first_name: Optional[str]
    last_name: Optional[str]
    preferences: Union[str, None] = None
    department: Union[str, None] = None
    city: Union[str, None] = None
    street: Union[str, None] = None
    building: Union[str, None] = None
    reason: Union[str, None] = None
