from typing import AsyncGenerator

from app.core.db import SessionLocal


async def get_db() -> AsyncGenerator:
    db = None
    try:
        db = SessionLocal(future=True)
        yield db
    finally:
        if db is not None:
            await db.close()
