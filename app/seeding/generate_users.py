from uuid import uuid4

from faker import Faker
from fastapi_users.password import get_password_hash

from app.core.db import database
from app.core.factory import Application
from app.models import User

fake = Faker('uk_UA')


async def generate_users():
    await database.connect()
    for i in range(100):
        values = {
            "id": uuid4(),
            "login": fake.first_name(),
            "email": fake.email(),
            "hashed_password": get_password_hash("TestingPassword"),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_playing": True,
            "department": "IT",
            "city": fake.city(),
            "street": fake.address().split(",")[0],
            "building": fake.building_number(),

            "is_active": 1,
            "is_superuser": 0,
            "is_verified": 1
        }
        await database.execute(query=User.__table__.insert(), values=values)
    await database.disconnect()
