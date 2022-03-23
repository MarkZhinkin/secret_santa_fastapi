import databases
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import registry, sessionmaker

from app.core.config import settings


engine = create_async_engine(settings.get_mysql_connection_string(), future=True)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession)

mapper_registry = registry()
database = databases.Database(settings.get_mysql_connection_string())
