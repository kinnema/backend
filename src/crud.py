from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.deps import CurrentUser
from src.core.security import hash_password, verify_password
from src.schemas import Favorites, User, UserCreate, FavoritesCreate, FavoritesDelete


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


async def get_favorites(*, session: AsyncSession, current_user: CurrentUser):
    favorites_query = select(Favorites, User).join(User).where(Favorites.user_id == current_user.id)
    favorites = await session.exec(favorites_query)

    favorites_with_user = favorites.scalars().all()
    return favorites_with_user


async def add_favorite(*, session: AsyncSession, current_user: CurrentUser, favorite: FavoritesCreate) -> Favorites:
    favorite = Favorites.model_validate(favorite, update={"user_id": current_user.id})
    session.add(favorite)
    await session.commit()
    await session.refresh(favorite)

    return favorite


async def delete_favorite(*, session: AsyncSession, current_user: CurrentUser, favorite: FavoritesDelete) -> bool:
    try:
        statement = select(Favorites).where(Favorites.id == favorite.favorite_id, Favorites.user_id == current_user.id)
        favorite = await session.exec(statement)
        favorite = favorite.first()

        await session.delete(favorite)
        await session.commit()

        return True
    except Exception:
        return False

