from fastapi import APIRouter, Depends, Response, status, HTTPException

from app.schemas.users_shemas import UserLogin, UserLoginResponse
from app.schemas.users_shemas import UC, UD

from app.depends.managers.user_manager import jwt_authentication, get_backend_strategy
from app.depends.managers.user_manager import UserManager, get_user_manager


router = APIRouter()


@router.post(
    "/login",
    response_model=UserLoginResponse,
    status_code=status.HTTP_201_CREATED,
    name="login",
)
async def login(
    user_login_item: UserLogin,
    response: Response,
    user_manager: UserManager[UC, UD] = Depends(get_user_manager)
):
    try:
        user = await user_manager.authenticate(user_login_item)
        bearer_response = await jwt_authentication.login(get_backend_strategy(), user, response)
        return bearer_response.__dict__

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.__repr__())
