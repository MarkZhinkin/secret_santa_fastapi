from app.schemas.users_shemas import User


class UserDB(User):
    hashed_password: str
