from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, BOOLEAN
from sqlalchemy import Column, text

from app.models.base import Base
from app.models.mixins import MysqlTimestampsMixin


class User(MysqlTimestampsMixin, Base, SQLAlchemyBaseUserTable):
    # alembic revision --autogenerate -m "add users table"
    __tablename__ = "users"

    login = Column(VARCHAR(length=255), unique=True, index=True, nullable=False)
    first_name = Column(VARCHAR(length=255), nullable=False, unique=False)
    last_name = Column(VARCHAR(length=255), nullable=False, unique=False)
    is_playing = Column(BOOLEAN(), nullable=False, unique=False, server_default=text("FALSE"))
    preferences = Column(TEXT(), nullable=True, unique=False)
    department = Column(VARCHAR(length=64), nullable=True, unique=False)
    city = Column(VARCHAR(length=64), nullable=True)
    street = Column(VARCHAR(length=128), nullable=True)
    building = Column(VARCHAR(length=16), nullable=True)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.email!r})"

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
