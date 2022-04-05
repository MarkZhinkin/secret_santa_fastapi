from app.schemas.emails_schemas import Email
from typing import Union


class EmailVerificationCodeResponse(Email):
    message_uid: str
    message: str


class EmailVerificationCodeConfirmRequest(Email):
    message_uid: str
    code: str


class EmailVerificationCodeConfirmResponse(Email):
    is_user_verified: bool = False
    reason: Union[str, None] = None
