from fastapi import APIRouter, Depends, status, HTTPException

from app.models.users_models import User
from app.schemas.games_schemas import G

from app.depends.managers.game_manager import GameManager, get_game_manager
from app.depends.managers.user_manager import verified_user
from app.schemas.users_schemas import GiftRecipientInfoResponse


router = APIRouter()


@router.get(
    "/gift_recipient_info",
    response_model=GiftRecipientInfoResponse,
    status_code=status.HTTP_200_OK,
    name="gift recipient info",
)
async def gift_recipient_info(
    game_manager: GameManager[G] = Depends(get_game_manager),
    user: User = Depends(verified_user),
):
    try:
        gift_recipient_info = await game_manager.get_gift_recipient_info(user)
        if gift_recipient_info is None:
            return GiftRecipientInfoResponse(reason="You don't have gift recipient.")
        return GiftRecipientInfoResponse(**gift_recipient_info)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())
