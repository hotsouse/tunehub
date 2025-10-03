from typing import Optional
from pydantic import BaseModel


# ==== AUTH / TOKEN ====
class TokenPayload(BaseModel):
    sub: Optional[str] = None


# ==== USER ====
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        orm_mode = True


class UserRead(UserInDB):
    pass


# ==== SONG ====
class SongBase(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    genre: Optional[str] = None


class SongCreate(SongBase):
    pass


class SongUpdate(SongBase):
    pass


class SongInDB(SongBase):
    id: int

    class Config:
        orm_mode = True


class SongRead(SongInDB):
    pass


# ==== PLAYLIST ====
class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistUpdate(PlaylistBase):
    pass


class PlaylistInDB(PlaylistBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class PlaylistRead(PlaylistInDB):
    pass
