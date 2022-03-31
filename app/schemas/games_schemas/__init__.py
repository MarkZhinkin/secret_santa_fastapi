from .game import Game
from .game_register import GameRegisterResponse, CancelGameRegisterResponse
from .game_open import GameOpenResponse
from .game_close import GameCloseResponse
from .game_playing_users import GamePlayingUsersResponse, GamePlayingUser
from .games_list import GamesListResponse, GameInfo
from .game_participants_pairs import GameParticipantsPairsResponse, ParticipantsPairs, GameParticipantsPairsRequest

from typing import TypeVar


G = TypeVar("G", bound=Game)
