from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.jwt_handler import create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.token import Token
from app.schemas.user import UserRegisterSchema
from app.services.user import UserService


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signup")
async def create_user(user: UserRegisterSchema):
    return await UserService().create_user(user)


@router.post("/login", response_model=Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await UserService().authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_role": str(user.user_role.value)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
