from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String

from app.models.base import Base
from app.models.mixins import MysqlTimestampsMixin


class User(MysqlTimestampsMixin, Base, SQLAlchemyBaseUserTable):
    # alembic revision --autogenerate -m "add users table"
    __tablename__ = "users"

    login = Column(String(length=255), unique=True, index=True, nullable=False)
    first_name = Column(String(length=255), nullable=False, unique=False)
    last_name = Column(String(length=255), nullable=False, unique=False)
    department = Column(String(length=64), nullable=True, unique=False)
    city = Column(String(length=64), nullable=True)
    street = Column(String(length=128), nullable=True)
    building = Column(String(length=16), nullable=True)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.email!r})"

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
