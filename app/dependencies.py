from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.schemas.token import TokenData
from .config import SECRET_KEY, ALGORITHM
from .models.user import Role
from .schemas.user import UserOutSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username, user_role = (
            payload.get("sub"),
            payload.get("user_role")
        )
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_role=user_role)
        return token_data
    except JWTError:
        raise credentials_exception


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return verify_token(token)


async def is_user_tourist(current_user: Annotated[UserOutSchema, Depends(get_current_user)]):
    if current_user.user_role != Role.TOURIST.value:
        raise HTTPException(status_code=405, detail="Not allowed")
    return current_user


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         user_role: str = payload.get("user_role")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username, user_role=user_role)
#     except JWTError:
#         raise credentials_exception
#     user = await UserService().get_user_by_username(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
