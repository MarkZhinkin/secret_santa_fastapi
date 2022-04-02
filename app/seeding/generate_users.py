from uuid import uuid4
import random as rand

from faker import Faker
from fastapi_users.password import get_password_hash

from app.core.db import database
from app.models import User

fake = Faker('uk_UA')

departments_list = ["Develop", "PM", "HR", "Service"]
login_list = []
email_list = []


async def generate_users(range_: int):
    await database.connect()
    for i in range(range_):
        values = {
            "id": uuid4(),
            "login": create_fake_login(),
            "email": create_fake_email(),
            "hashed_password": get_password_hash("TestingPassword"),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_playing": True,
            "department": rand.choice(departments_list),
            "city": fake.city(),
            "street": fake.address().split(",")[0],
            "building": fake.building_number(),

            "is_active": 1,
            "is_superuser": 0,
            "is_verified": 1
        }
        await database.execute(query=User.__table__.insert(), values=values)
    await database.disconnect()


def create_fake_login():
    while True:
        login = fake.first_name()
        if login not in login_list:
            login_list.append(login)
            return login


def create_fake_email():
    while True:
        email = fake.email()
        if email not in email_list:
            email_list.append(email)
            return email
