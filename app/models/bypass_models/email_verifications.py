from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP
from sqlalchemy import Column, String

from app.models.base import Base
from app.models.mixins import MysqlTimestampsMixin


class EmailVerification(Base, MysqlTimestampsMixin):
    # alembic revision --autogenerate -m "add email verifications table"
    __tablename__ = "email_verifications"

    id = Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    email = Column(String(length=320), index=True, nullable=False)
    code = Column(String(length=16), unique=False, nullable=False)
    message_uid = Column(String(length=128), unique=True, nullable=False, index=True)
    deleted_at = Column(TIMESTAMP, nullable=True, index=True, default=None)

    def __repr__(self):
        return f"EmailVerification(id={self.id!r}, email={self.email!r})"
