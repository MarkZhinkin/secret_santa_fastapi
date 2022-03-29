from fastapi import APIRouter

from . import email_verification


user_router = APIRouter(prefix='/user')

user_router.include_router(email_verification.router)
