from fastapi import APIRouter
from endpoints import login, user
api_router = APIRouter()
api_router.include_router(login.router, tags=["login"], prefix='/login')
api_router.include_router(user.router, tags=["user"], prefix='/user')