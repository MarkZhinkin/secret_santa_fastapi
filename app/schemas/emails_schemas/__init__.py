from .email import Email
from .email_verification_code import (
    EmailVerificationCodeResponse,
    EmailVerificationCodeConfirmRequest,
    EmailVerificationCodeConfirmResponse
)

from typing import TypeVar


EVCCRQ = TypeVar("EVCCRQ", bound=EmailVerificationCodeConfirmRequest)
