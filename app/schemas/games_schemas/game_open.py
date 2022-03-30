from app.schemas.games_schemas import Game


class GameOpenResponse(Game):
    is_game_open: bool = False
