from fastapi_users.models import CreateUpdateDictModel


class Game(CreateUpdateDictModel):
    class Config:
        orm_mode = True
