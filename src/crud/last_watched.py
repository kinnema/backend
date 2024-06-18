from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.deps import CurrentUser
from src.models import LastWatchedCreate
from src.schemas import LastWatched


class LastWatchedCrud:
    @staticmethod
    async def get_last_watched(*, session: AsyncSession, current_user: CurrentUser):
        last_watched_query = select(LastWatched).where(
            LastWatched.user_id == current_user.id,
            LastWatched.is_watched == False,  # noqa: E712
        )
        last_watched = await session.exec(last_watched_query)

        return last_watched.all()

    @staticmethod
    async def _get_single_last_watched(
        *, session: AsyncSession, current_user: CurrentUser, tmdb_id: int
    ):
        last_watched_query = select(LastWatched).where(
            LastWatched.user_id == current_user.id,
            LastWatched.is_watched == False,  # noqa: E712
        )
        last_watched = await session.exec(last_watched_query)

        return last_watched.first()

    @staticmethod
    async def add_last_watched(
        *,
        session: AsyncSession,
        current_user: CurrentUser,
        last_watched: LastWatchedCreate,
    ):
        last_watched_query = await LastWatchedCrud._get_single_last_watched(
            session=session, current_user=current_user, tmdb_id=last_watched.tmdb_id
        )

        if last_watched_query:
            return

        last_watched_query = LastWatched.model_validate(
            last_watched, update={"user_id": current_user.id}
        )

        session.add(last_watched_query)
        await session.commit()
        await session.refresh(last_watched_query)

        return last_watched_query

    @staticmethod
    async def mark_last_watched(
        *,
        session: AsyncSession,
        current_user: CurrentUser,
        id: int,
    ):
        last_watched_query = select(LastWatched).where(
            LastWatched.id == id,
            LastWatched.user_id == current_user.id,
            LastWatched.is_watched == False,  # noqa: E712
        )
        last_watched = await session.exec(last_watched_query)

        last_watched = last_watched.first()

        if last_watched:
            last_watched.is_watched = True
            await session.commit()
            await session.refresh(last_watched)

        return last_watched
