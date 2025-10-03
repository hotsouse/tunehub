from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# ======== Модель песни ========
class Song(BaseModel):
    id: int = None  # теперь id необязательный
    title: str
    artist: str
    favorite: bool = False

# ======== Временная база ========
songs_db: List[Song] = [
    Song(id=1, title="Shape of You", artist="Ed Sheeran"),
    Song(id=2, title="Blinding Lights", artist="The Weeknd"),
    Song(id=3, title="Levitating", artist="Dua Lipa"),
]

# ======== CRUD для песен ========
# Получить список всех песен
@router.get("/", response_model=List[Song])
async def get_songs():
    return songs_db

# Добавить новую песню с авто-ID
@router.post("/", response_model=Song)
async def add_song(song: Song):
    # Генерируем новый ID
    new_id = max([s.id for s in songs_db], default=0) + 1
    song.id = new_id
    songs_db.append(song)
    return song

# Удалить песню по ID
@router.delete("/{song_id}")
async def delete_song(song_id: int):
    global songs_db
    if not any(s.id == song_id for s in songs_db):
        raise HTTPException(status_code=404, detail="Song not found")
    songs_db = [s for s in songs_db if s.id != song_id]
    return {"message": "Song deleted"}

# Добавить песню в избранное
@router.post("/{song_id}/favorite")
async def add_favorite(song_id: int):
    for song in songs_db:
        if song.id == song_id:
            song.favorite = True
            return {"message": "Added to favorites"}
    raise HTTPException(status_code=404, detail="Song not found")
