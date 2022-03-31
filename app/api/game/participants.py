from fastapi import APIRouter, Depends, status, HTTPException

from app.models.users_models import User
from app.schemas.games_schemas import (
    G,
    GamePlayingUsersResponse, GamePlayingUser,
    GamesListResponse, GameInfo,
    GameParticipantsPairsResponse, ParticipantsPairs, GameParticipantsPairsRequest
)
from app.schemas.users_schemas import UC, UD

from app.depends.managers.user_manager import admin_user
from app.depends.managers.game_manager import GameManager, get_game_manager
from app.depends.managers.user_manager import UserManager, get_user_manager


router = APIRouter()


@router.get(
    "/playing_users",
    response_model=GamePlayingUsersResponse,
    status_code=status.HTTP_200_OK,
    name="playing users",
)
async def playing_users(
    user_manager: UserManager[UC, UD] = Depends(get_user_manager),
    user: User = Depends(admin_user),
):
    try:
        playing_users_list = await user_manager.get_playing_users()
        return GamePlayingUsersResponse(
            playing_users_list=[GamePlayingUser(**playing_user) for playing_user in playing_users_list]
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())


@router.get(
    "/games_list",
    response_model=GamesListResponse,
    status_code=status.HTTP_200_OK,
    name="games list",
)
async def games_list(
    game_manager: GameManager[G] = Depends(get_game_manager),
    user: User = Depends(admin_user),
):
    try:
        games_list = await game_manager.get_games_list()
        return GamesListResponse(
            games_list=[GameInfo(**games) for games in games_list]
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())


@router.get(
    "/participants_pairs",
    response_model=GameParticipantsPairsResponse,
    status_code=status.HTTP_200_OK,
    name="participants pairs",
)
async def participants_pairs(
    game_participants_pairs_item: GameParticipantsPairsRequest,
    game_manager: GameManager[G] = Depends(get_game_manager),
    user: User = Depends(admin_user),
):
    try:
        participants_pairs = await game_manager.get_participants_pairs(game_participants_pairs_item.year)
        return GameParticipantsPairsResponse(
            playing_users_list=[ParticipantsPairs(**participants_pair) for participants_pair in participants_pairs]
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())
