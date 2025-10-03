from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    playlists: List["Playlist"] = Relationship(back_populates="owner")
    favorites: List["Favorite"] = Relationship(back_populates="user")

class Artist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, unique=True)
    songs: List["Song"] = Relationship(back_populates="artist_rel")

class Genre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, unique=True)
    songs: List["Song"] = Relationship(back_populates="genre_rel")

class Song(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, index=True)
    artist_id: Optional[int] = Field(default=None, foreign_key="artist.id")
    genre_id: Optional[int] = Field(default=None, foreign_key="genre.id")
    url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    artist_rel: Optional[Artist] = Relationship(back_populates="songs")
    genre_rel: Optional[Genre] = Relationship(back_populates="songs")
    favorites: List["Favorite"] = Relationship(back_populates="song")

class Playlist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional[User] = Relationship(back_populates="playlists")
    items: List["PlaylistItem"] = Relationship(back_populates="playlist")

class PlaylistItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    playlist_id: int = Field(foreign_key="playlist.id")
    song_id: int = Field(foreign_key="song.id")
    added_at: datetime = Field(default_factory=datetime.utcnow)

    playlist: Optional[Playlist] = Relationship(back_populates="items")
    # No relationship back to Song to keep it simple

class Favorite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    song_id: int = Field(foreign_key="song.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="favorites")
    song: Optional[Song] = Relationship(back_populates="favorites")
