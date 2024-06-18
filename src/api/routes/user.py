from typing import List

from fastapi import APIRouter, HTTPException, status

from src.api.deps import CurrentUser, SessionDep
from src.crud.favorites import FavoritesCrud
from src.crud.last_watched import LastWatchedCrud
from src.models import LastWatchedCreate
from src.schemas import (
    Favorites,
    FavoritesCreate,
    FavoritesDelete,
    FavoritesPublic,
    LastWatchedResponse,
)

router = APIRouter()


@router.get(
    "/last_watched",
    response_model=List[LastWatchedResponse],
)
async def user_last_watched(*, session: SessionDep, current_user: CurrentUser):
    s = await LastWatchedCrud.get_last_watched(
        session=session, current_user=current_user
    )

    return s


@router.post("/last_watched")
async def add_last_watched(
    *, session: SessionDep, current_user: CurrentUser, last_watched: LastWatchedCreate
):
    s = await LastWatchedCrud.add_last_watched(
        session=session, current_user=current_user, last_watched=last_watched
    )

    return s


@router.post("/last_watched/{id}/mark")
async def mark_last_watched(*, session: SessionDep, current_user: CurrentUser, id: int):
    s = await LastWatchedCrud.mark_last_watched(
        session=session, current_user=current_user, id=id
    )

    return s


@router.get("/favorites", response_model=List[FavoritesPublic])
async def user_favorites(*, session: SessionDep, current_user: CurrentUser):
    return await FavoritesCrud.get_favorites(session=session, current_user=current_user)


@router.post("/favorites")
async def add_favorite(
    *, session: SessionDep, current_user: CurrentUser, favorite: FavoritesCreate
) -> Favorites:
    return await FavoritesCrud.add_favorite(
        session=session, current_user=current_user, favorite_create=favorite
    )


@router.delete("/favorites")
async def delete_favorite(
    *, session: SessionDep, current_user: CurrentUser, favorite: FavoritesDelete
) -> bool:
    delete = await FavoritesCrud.delete_favorite(
        session=session, current_user=current_user, favorite_create=favorite
    )

    if not delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found"
        )

    return True
