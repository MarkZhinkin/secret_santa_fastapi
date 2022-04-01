from fastapi import APIRouter, Depends, status, HTTPException

from app.models.users_models import User
from app.schemas.users_schemas import UC, UD
from app.schemas.games_schemas import G

from app.depends.managers.user_manager import UserManager, get_user_manager, verified_user
from app.schemas.games_schemas import GameRegisterResponse, CancelGameRegisterResponse
from app.depends.managers.game_manager import GameManager, get_game_manager

router = APIRouter()


@router.get(
    "/register",
    response_model=GameRegisterResponse,
    status_code=status.HTTP_200_OK,
    name="register",
)
async def register(
    user_manager: UserManager[UC, UD] = Depends(get_user_manager),
    game_manager: GameManager[G] = Depends(get_game_manager),
    user: User = Depends(verified_user),
):
    try:
        if not user.is_superuser:
            if await game_manager.get_current_game():
                await user_manager.change_user_info(user, {"is_playing": True})
                return GameRegisterResponse(is_register_to_game=True)
            else:
                return GameRegisterResponse(reason="Game is unavailable.")
        else:
            return GameRegisterResponse(reason="Administrator can't play in secret santa.")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())


@router.get(
    "/cancel",
    response_model=CancelGameRegisterResponse,
    status_code=status.HTTP_200_OK,
    name="cancel",
)
async def cancel(
    user_manager: UserManager[UC, UD] = Depends(get_user_manager),
    game_manager: GameManager[G] = Depends(get_game_manager),
    user: User = Depends(verified_user),
):
    try:
        if not user.is_superuser:
            if await game_manager.get_current_game():
                await user_manager.change_user_info(user, {"is_playing": False})
                return CancelGameRegisterResponse(is_cancel_register_to_game=True)
            else:
                return GameRegisterResponse(reason="Game is unavailable.")
        else:
            return GameRegisterResponse(reason="Administrator can't play in secret santa.")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())
