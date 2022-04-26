from fastapi import APIRouter, Depends, status, HTTPException

from app.models.users_models import User
from app.schemas.games_schemas import G, GameOpenResponse

from app.depends.managers.user_manager import admin_user
from app.depends.managers.game_manager import GameManager, get_game_manager


router = APIRouter()


@router.get(
    "/open_game",
    response_model=GameOpenResponse,
    status_code=status.HTTP_200_OK,
    name="open game",
)
async def open_game(
    game_manager: GameManager[G] = Depends(get_game_manager),
    user: User = Depends(admin_user),
):
    """
        **Superusers only**\n
        Superusers can start only one game in current year.\n
        If game already exist user will get alert.
    """
    try:
        await game_manager.open_game()
        return GameOpenResponse(is_game_open=True)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())
