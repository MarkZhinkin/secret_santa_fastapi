from fastapi import APIRouter, Depends, status, HTTPException

from app.models.users_models import User
from app.schemas.users_schemas import UC, UD

from app.utils.sendgrid_post_office import SendgridPostOffice


from app.depends.managers.user_manager import UserManager, get_user_manager, unverified_user
from app.schemas.emails_schemas import (
    EmailVerificationCodeResponse,
    EmailVerificationCodeConfirmRequest,
    EmailVerificationCodeConfirmResponse
)


router = APIRouter()


@router.get(
    "/send_code",
    response_model=EmailVerificationCodeResponse,
    status_code=status.HTTP_200_OK,
    name="send code",
)
async def send_code(
    user_manager: UserManager[UC, UD] = Depends(get_user_manager),
    user: User = Depends(unverified_user),
):
    try:
        user_email = user.email
        send_grid = SendgridPostOffice()
        send_status, code, message_uid = send_grid.email_confirmation_send_message(user_email)

        if send_status >= 400:
            raise Exception(f"Verification code didn't send, {send_status}.")

        is_added = await user_manager.add_verification_code(email=user_email, code=code, message_uid=message_uid)
        if not is_added:
            raise Exception("Verification code didn't add.")

        return EmailVerificationCodeResponse(message_uid=message_uid)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())


@router.post(
    "/confirmation_code",
    response_model=EmailVerificationCodeConfirmResponse,
    status_code=status.HTTP_200_OK,
    name="confirmation code",
)
async def confirmation_code(
    verification_code_item: EmailVerificationCodeConfirmRequest,
    user_manager: UserManager[UC, UD] = Depends(get_user_manager),
    user: User = Depends(unverified_user),
):
    try:
        verification_code_row = await user_manager.get_verification_code_by_id(verification_code_item)
        if verification_code_row is None:
            return EmailVerificationCodeConfirmResponse(reason="Verification code undefined.")

        await user_manager.delete_verification_code(verification_code_item.message_uid)
        await user_manager.change_user_right(user)

        return EmailVerificationCodeConfirmResponse(is_user_verified=True)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())

