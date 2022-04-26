from app.schemas.emails_schemas import Email
from typing import Union


class EmailVerificationCodeResponse(Email):
    message_uid: str
    message: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "message_uid": "tgq2pt7jm8xmfgni9",
                "message": "On stage a message would be sent to your mail with the following content: 123456"
            }
        }


class EmailVerificationCodeConfirmRequest(Email):
    message_uid: str
    code: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "message_uid": "tgq2pt7jm8xmfgni9",
                "message": "123456"
            }
        }


class EmailVerificationCodeConfirmResponse(Email):
    is_user_verified: bool = False
    reason: Union[str, None] = None

    class Config:
        schema_extra = {
            "example": {
                "is_user_verified": True,
                "message": None
            }
        }
