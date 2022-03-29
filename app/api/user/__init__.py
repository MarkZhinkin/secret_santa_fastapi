from fastapi import APIRouter

from . import email_verification, user_info


user_router = APIRouter(prefix='/user')

user_router.include_router(email_verification.router)
user_router.include_router(user_info.router)
