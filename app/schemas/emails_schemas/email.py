from fastapi_users.models import CreateUpdateDictModel


class Email(CreateUpdateDictModel):
    class Config:
        orm_mode = True
