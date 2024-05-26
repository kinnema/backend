from typing import Optional

from sqlmodel import Field, SQLModel


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


class UserPublic(UserBase):
    id: int

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
