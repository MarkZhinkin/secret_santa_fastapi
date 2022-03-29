from fastapi_users.models import CreateUpdateDictModel


class User(CreateUpdateDictModel):
    class Config:
        orm_mode = True
