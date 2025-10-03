from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routers import songs, playlists, admin

app = FastAPI()

# Подключаем роутеры (API)
app.include_router(songs.router, prefix="/api/songs", tags=["songs"])
app.include_router(playlists.router, prefix="/api/playlists", tags=["playlists"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

# Настройка шаблонов
templates = Jinja2Templates(directory="app/templates")

# --- Роуты для HTML страниц ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/songs", response_class=HTMLResponse)
def songs_page(request: Request):
    return templates.TemplateResponse("songs.html", {"request": request})

@app.get("/playlists", response_class=HTMLResponse)
def playlists_page(request: Request):
    return templates.TemplateResponse("playlists.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
