from fastapi import APIRouter

from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/")
async def get_users():
    return await UserService().get_users()


@router.get("/me")
async def get_me():
    pass
