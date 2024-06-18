from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    username: str
    email: str
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    favorites: list["Favorites"] = Relationship(back_populates="user")
    last_watched: list["LastWatched"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: int


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    access_token: str
    user: UserPublic


class FavoritesBase(SQLModel):
    tmdb_id: int
    name: str
    poster_path: str


class FavoritesCreate(FavoritesBase):
    pass


class FavoritesDelete(BaseModel):
    favorite_id: int


class Favorites(FavoritesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(
        back_populates="favorites",
    )


class FavoritesPublic(FavoritesBase):
    user: UserPublic


class LastWachedBase(SQLModel):
    name: str
    slug: str
    poster_path: str
    season: int
    episode: int
    is_watched: bool = False
    tmdb_id: int
    network: int | None = None


class LastWatched(LastWachedBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(
        back_populates="last_watched",
    )


class LastWatchedResponse(LastWachedBase):
    user: UserPublic
    id: int
