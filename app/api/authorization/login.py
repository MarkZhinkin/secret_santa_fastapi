from fastapi import APIRouter, Depends, Response, status, HTTPException

from app.schemas.users_schemas import UserLogin, UserLoginResponse
from app.schemas.users_schemas import UC, UD

from app.depends.managers.user_manager import jwt_authentication
from app.depends.managers.user_manager import UserManager, get_user_manager


router = APIRouter()


@router.post(
    "/login",
    response_model=UserLoginResponse,
    status_code=status.HTTP_200_OK,
    name="login"
)
async def login(
    user_login_item: UserLogin,
    response: Response,
    user_manager: UserManager[UC, UD] = Depends(get_user_manager)
):
    """
        The router that helps users log in and access the site.
    """
    try:
        user = await user_manager.authenticate(user_login_item)
        bearer_response = await jwt_authentication.get_login_response(user, response, user_manager)
        return bearer_response.__dict__

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.__repr__())
