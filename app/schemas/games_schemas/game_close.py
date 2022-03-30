from app.schemas.games_schemas import Game


class GameCloseResponse(Game):
    is_game_close: bool = False