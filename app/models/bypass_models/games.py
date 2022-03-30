from sqlalchemy.dialects.mysql import TIMESTAMP, BOOLEAN, SMALLINT
from sqlalchemy import Column, text

from app.models.base import Base
from app.models.mixins import MysqlTimestampsMixin, MysqlPrimaryKeyMixin


class Game(Base, MysqlPrimaryKeyMixin, MysqlTimestampsMixin):
    # alembic revision --autogenerate -m "add games table"
    __tablename__ = "games"

    game_year = Column(SMALLINT(unsigned=True), index=True, nullable=False)
    is_registration_open = Column(BOOLEAN(), index=True, nullable=False, server_default=text("FALSE"))
    registration_opened_at = Column(TIMESTAMP, nullable=True)
    is_registration_close = Column(BOOLEAN(), index=True, nullable=False, server_default=text("FALSE"))
    registration_closed_at = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return f"Game(id={self.id!r}, game_year={self.game_year!r})"
