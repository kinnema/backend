from typing import List

from fastapi import APIRouter, HTTPException, status

from src import crud
from src.api.deps import CurrentUser, SessionDep
from src.schemas import FavoritesCreate, FavoritesPublic, FavoritesDelete, Favorites

router = APIRouter()


@router.get("/favorites",  response_model=List[FavoritesPublic])
async def user_favorites(*, session: SessionDep, current_user: CurrentUser):
    return await crud.get_favorites(session=session, current_user=current_user)


@router.post("/favorites")
async def add_favorite(*, session: SessionDep, current_user: CurrentUser, favorite: FavoritesCreate) -> Favorites:
    return await crud.add_favorite(session=session, current_user=current_user, favorite=favorite)


@router.delete("/favorites")
async def delete_favorite(*, session: SessionDep, current_user: CurrentUser, favorite: FavoritesDelete) -> bool:
    delete = await crud.delete_favorite(session=session, current_user=current_user, favorite=favorite)

    if not delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")

    return True