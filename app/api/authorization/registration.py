from fastapi import APIRouter, Depends, Response, status, HTTPException

from app.depends.managers.user_manager import jwt_authentication

from app.schemas.users_schemas import UserCreate, UserCreateResponse
from app.schemas.users_schemas import UC, UD
from app.depends.managers.user_manager import UserManager, get_user_manager


router = APIRouter()


@router.post(
    "/register",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
    name="register",
)
async def register(
    user_create_item: UserCreate,
    response: Response,
    user_manager: UserManager[UC, UD] = Depends(get_user_manager)
):
    """
        The router for registering new users.
    """
    try:
        user_manager.validate_login_and_password(user_create_item.login, user_create_item.password)
        user = await user_manager.create(user=user_create_item, safe=True)
        bearer_response = await jwt_authentication.get_login_response(user, response, user_manager)
        return bearer_response.__dict__

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.__repr__())
