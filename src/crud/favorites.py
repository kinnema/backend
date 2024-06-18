from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.deps import CurrentUser
from src.schemas import Favorites, FavoritesCreate, FavoritesDelete


class FavoritesCrud:
    @staticmethod
    async def get_favorites(*, session: AsyncSession, current_user: CurrentUser):
        favorites_query = select(Favorites).where(Favorites.user_id == current_user.id)
        favorites = await session.exec(favorites_query)

        return favorites.all()

    @staticmethod
    async def add_favorite(
        *,
        session: AsyncSession,
        current_user: CurrentUser,
        favorite_create: FavoritesCreate,
    ) -> Favorites:
        favorite = Favorites.model_validate(
            favorite_create, update={"user_id": current_user.id}
        )
        session.add(favorite)
        await session.commit()
        await session.refresh(favorite)

        return favorite

    @staticmethod
    async def delete_favorite(
        *,
        session: AsyncSession,
        current_user: CurrentUser,
        favorite_create: FavoritesDelete,
    ) -> bool:
        try:
            statement = select(Favorites).where(
                Favorites.id == favorite_create.favorite_id,
                Favorites.user_id == current_user.id,
            )
            favorite = await session.exec(statement)
            favorite = favorite.first()

            await session.delete(favorite)
            await session.commit()

            return True
        except Exception:
            return False
