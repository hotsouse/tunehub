from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select, Session
from app.db import get_session
from app.deps import get_current_active_user
from app.models import Playlist, PlaylistItem, Song
from app.schemas import SongRead

router = APIRouter(prefix="/playlists", tags=["playlists"])

# ======== Создать новый плейлист ========
@router.post("/", response_model=dict)
def create_playlist(
    name: str, 
    current_user = Depends(get_current_active_user), 
    session: Session = Depends(get_session)
):
    pl = Playlist(name=name, user_id=current_user.id)
    session.add(pl)
    session.commit()
    session.refresh(pl)
    return {"id": pl.id, "name": pl.name, "songs": []}

# ======== Добавить песню в плейлист ========
@router.post("/{playlist_id}/add", response_model=dict)
def add_song_to_playlist(
    playlist_id: int, 
    song_id: int, 
    current_user = Depends(get_current_active_user), 
    session: Session = Depends(get_session)
):
    pl = session.get(Playlist, playlist_id)
    if not pl or pl.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Playlist not found or access denied")
    
    song = session.get(Song, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    existing_item = session.exec(
        select(PlaylistItem).where(
            PlaylistItem.playlist_id == playlist_id,
            PlaylistItem.song_id == song_id
        )
    ).first()
    
    if not existing_item:
        item = PlaylistItem(playlist_id=playlist_id, song_id=song_id)
        session.add(item)
        session.commit()
    
    # Возвращаем актуальный список песен
    items = session.exec(
        select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id)
    ).all()
    songs_in_playlist = [SongRead.from_orm(session.get(Song, it.song_id)) for it in items]

    return {"id": pl.id, "name": pl.name, "songs": songs_in_playlist}

# ======== Удалить песню из плейлиста ========
@router.delete("/{playlist_id}/remove/{song_id}", response_model=dict)
def remove_song_from_playlist(
    playlist_id: int, 
    song_id: int, 
    current_user = Depends(get_current_active_user), 
    session: Session = Depends(get_session)
):
    pl = session.get(Playlist, playlist_id)
    if not pl or pl.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Playlist not found or access denied")

    item = session.exec(
        select(PlaylistItem).where(
            PlaylistItem.playlist_id == playlist_id,
            PlaylistItem.song_id == song_id
        )
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Song not in playlist")
    
    session.delete(item)
    session.commit()

    items = session.exec(
        select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id)
    ).all()
    songs_in_playlist = [SongRead.from_orm(session.get(Song, it.song_id)) for it in items]

    return {"id": pl.id, "name": pl.name, "songs": songs_in_playlist}

# ======== Удалить плейлист ========
@router.delete("/{playlist_id}", response_model=dict)
def delete_playlist(
    playlist_id: int, 
    current_user = Depends(get_current_active_user), 
    session: Session = Depends(get_session)
):
    pl = session.get(Playlist, playlist_id)
    if not pl or pl.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Playlist not found or access denied")
    
    items = session.exec(
        select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id)
    ).all()
    for it in items:
        session.delete(it)

    session.delete(pl)
    session.commit()

    return {"status": "Playlist deleted"}

# ======== Получить все плейлисты с песнями ========
@router.get("/", response_model=List[dict])
def list_playlists(
    current_user = Depends(get_current_active_user), 
    session: Session = Depends(get_session)
):
    pls = session.exec(
        select(Playlist).where(Playlist.user_id == current_user.id)
    ).all()
    
    out = []
    for p in pls:
        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == p.id)
        ).all()
        songs_in_playlist = [SongRead.from_orm(session.get(Song, it.song_id)) for it in items]
        out.append({"id": p.id, "name": p.name, "songs": songs_in_playlist})

    return out
