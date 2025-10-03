from fastapi import APIRouter, Depends, HTTPException
from app.deps import get_current_superuser
from app.db import get_session
from sqlmodel import Session, select
from app.models import Artist, Genre

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(get_current_superuser)])

@router.post("/artists")
def create_artist(name: str, session: Session = Depends(get_session)):
    q = select(Artist).where(Artist.name == name)
    exists = session.exec(q).first()
    if exists:
        raise HTTPException(status_code=400, detail="Artist exists")
    a = Artist(name=name)
    session.add(a)
    session.commit()
    session.refresh(a)
    return a

@router.post("/genres")
def create_genre(name: str, session: Session = Depends(get_session)):
    q = select(Genre).where(Genre.name == name)
    exists = session.exec(q).first()
    if exists:
        raise HTTPException(status_code=400, detail="Genre exists")
    g = Genre(name=name)
    session.add(g)
    session.commit()
    session.refresh(g)
    return g
