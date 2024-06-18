from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.security import hash_password, verify_password
from src.schemas import User, UserCreate


async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = await session.exec(statement)
    return session_user.first()


async def create_user(*, session: AsyncSession, user: UserCreate) -> User:
    db_user = User.model_validate(
        user, update={"hashed_password": hash_password(user.password)}
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def authenticate(
    *, session: AsyncSession, email: str, password: str
) -> User | None:
    db_user = await get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
