from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src import crud
from src.api.deps import CurrentUser, SessionDep
from src.core.config import settings
from src.core.security import create_access_token
from src.schemas import Token, User, UserCreate, UserPublic

router = APIRouter()

@router.post("/register", response_model=UserPublic)
async def register(*, session: SessionDep, user: UserCreate):
    user_db = await crud.get_user_by_email(session=session, email=user.email)

    if user_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await crud.create_user(session=session, user=user)


@router.post("/login", )
async def login(*, session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await crud.authenticate(session=session, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )

@router.get("/me", response_model=UserPublic)
async def get_current_user(user: CurrentUser):
    return user