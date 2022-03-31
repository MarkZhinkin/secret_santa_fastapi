from uuid import uuid4

from fastapi_users.password import get_password_hash

from app.core.db import database
from app.models import User


async def generate_admin():
    await database.connect()
    for i in range(100):
        values = {
            "id": uuid4(),
            "login": "Santa Claus",
            "email": "santa@gmail.com",
            "hashed_password": get_password_hash("HappyNewYear!123@#$"),
            "first_name": "Saint",
            "last_name": "Mykolai",
            "is_playing": False,
            "department": "Christmas ad Happy",
            "is_active": 1,
            "is_superuser": 1,
            "is_verified": 1
        }
        await database.execute(query=User.__table__.insert(), values=values)
    await database.disconnect()
