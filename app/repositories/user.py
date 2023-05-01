from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.user import User
from app.schemas.user import UserDBSchema, UserOutSchema


class UserRepository:

    def __init__(self):
        self.session: AsyncSession = async_session()

    async def create_user(self, user: UserDBSchema):
        stmt = insert(User).values(**user.dict())
        await self.session.execute(stmt)
        await self.session.commit()
        return {"status": "success"}

    async def get_user_by_username(self, username: str) -> Optional[UserDBSchema]:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()
        if user:
            return UserDBSchema.from_orm(user)
        return user

    async def get_user_by_email(self, email: str) -> Optional[UserOutSchema]:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()
        if user:
            return UserOutSchema.from_orm(user)
        return user

    async def get_list_users(self) -> Optional[list[UserOutSchema]]:
        query = select(User).limit(10)
        result = await self.session.execute(query)
        users = result.scalars().all()
        user_list = []
        for user in users:
            user_list.append(UserOutSchema.from_orm(user))
        return user_list
