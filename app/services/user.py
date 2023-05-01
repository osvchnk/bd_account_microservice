from typing import Optional

from fastapi import HTTPException
from passlib.context import CryptContext

from app.repositories.user import UserRepository
from app.schemas.user import UserRegisterSchema, UserDBSchema, UserOutSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self):
        self.repository: UserRepository = UserRepository()

    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def create_user(self, user: UserRegisterSchema):
        if await self.repository.get_user_by_username(username=user.username) is not None:
            raise HTTPException(status_code=409, detail=f"Username '{user.username}' is already taken")

        if await self.repository.get_user_by_email(email=user.email) is not None:
            raise HTTPException(status_code=409, detail=f"Email '{user.email}' is already taken")

        return await self.repository.create_user(UserDBSchema(**user.dict(),
                                                              hashed_password=self.hash_password(user.password)
                                                              ))

    async def get_user_by_username(self, username: str) -> Optional[UserOutSchema]:
        user = await self.repository.get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User not found")
        return UserOutSchema(**user.dict())

    async def authenticate_user(self, username: str, password: str):
        user = await self.repository.get_user_by_username(username=username)
        if not user:
            return False
        if not self.verify_password(plain_password=password,
                                    hashed_password=user.hashed_password):
            return False
        return user

    async def get_users(self):
        result = await self.repository.get_list_users()
        if not result:
            return {"result": "no users"}
        return result
