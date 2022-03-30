from fastapi import APIRouter, Depends, status, HTTPException

from app.models.users_models import User
from app.schemas.games_schemas import G, GameCloseResponse

from app.depends.managers.user_manager import admin_user
from app.depends.managers.game_manager import GameManager, get_game_manager


router = APIRouter()


@router.get(
    "/close_game",
    response_model=GameCloseResponse,
    status_code=status.HTTP_200_OK,
    name="close game",
)
async def close_game(
    game_manager: GameManager[G] = Depends(get_game_manager),
    user: User = Depends(admin_user),
):
    try:
        await game_manager.close_game()
        # ToDo Create new participants
        return GameCloseResponse(is_game_close=True)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())
