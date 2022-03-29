from fastapi import APIRouter, Depends, status, HTTPException

from app.models.users_models import User
from app.schemas.users_shemas import UC, UD

from app.depends.managers.user_manager import UserManager, get_user_manager, unverified_user, verified_user
from app.schemas.users_shemas import (
    UserInfoResponse,
    UserInfoChangeRequest,
    UserInfoChangeResponse
)


router = APIRouter()


@router.get(
    "/me",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK,
    name="me",
)
async def me(
    user_manager: UserManager[UC, UD] = Depends(get_user_manager),
    user: User = Depends(unverified_user),
):
    try:
        user_info = await user_manager.get_user_info(user)
        return UserInfoResponse(**user_info)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())


@router.post(
    "/change_user_info",
    response_model=UserInfoChangeResponse,
    status_code=status.HTTP_200_OK,
    name="change_user_info",
)
async def change_user_info(
    user_info_item: UserInfoChangeRequest,
    user_manager: UserManager[UC, UD] = Depends(get_user_manager),
    user: User = Depends(verified_user),
):
    try:
        await user_manager.change_preferences(user=user, user_info_item=user_info_item.dict())
        return UserInfoChangeResponse(is_info_change=True)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())
