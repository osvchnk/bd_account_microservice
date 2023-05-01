from pydantic import BaseModel, EmailStr

from app.models.user import Role


class UserBaseSchema(BaseModel):
    username: str


class UserLoginSchema(UserBaseSchema):
    password: str


class UserRegisterSchema(UserLoginSchema):
    email: EmailStr
    first_name: str | None
    second_name: str | None


class UserDBSchema(UserBaseSchema):
    hashed_password: str
    email: EmailStr
    first_name: str | None
    second_name: str | None
    user_role: Role

    class Config:
        orm_mode = True


class UserOutSchema(UserBaseSchema):
    email: EmailStr
    first_name: str | None
    second_name: str | None
    user_role: Role

    class Config:
        orm_mode = True
