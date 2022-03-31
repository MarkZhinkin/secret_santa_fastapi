from sqlalchemy.dialects.mysql import BIGINT, TEXT
from sqlalchemy import Column

from fastapi_users_db_sqlalchemy import GUID

from app.models.base import Base
from app.models.mixins import MysqlTimestampsMixin, MysqlPrimaryKeyMixin


class Participant(Base, MysqlPrimaryKeyMixin, MysqlTimestampsMixin):
    # alembic revision --autogenerate -m "add participants table"
    __tablename__ = "participants"

    game_id = Column(BIGINT(unsigned=True), index=True, nullable=False, unique=False)
    secret_santa_id = Column(GUID(), index=True, nullable=False, unique=False)
    gift_recipient_id = Column(GUID(), index=True, nullable=True, unique=False)
    preferences = Column(TEXT(), index=False, nullable=True, unique=False)

    def __repr__(self):
        return f"Participant(id={self.id!r}, game_id={self.game_id!r})"
