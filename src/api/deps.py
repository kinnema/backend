from typing import Annotated, Generator

import jwt
from fastapi import Depends, HTTPException, security, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import settings
from src.core.database import engine
from src.core.security import ALGORITHM
from src.models import TokenPayload
from src.schemas import User


def get_db() -> AsyncSession:
    return AsyncSession(engine)


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/auth/login/access-token"
)


SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
