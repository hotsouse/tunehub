# Music Catalog

Django-приложение каталога музыки с аутентификацией, плейлистами, REST API, Swagger, Docker и CI.

## Как запустить

### Вариант 1: Docker
```bash
docker-compose up --build
# Создать админа (опционально):
docker-compose exec web python manage.py createsuperuser
```
Открыть: `http://localhost:8000`

### Вариант 2: Локально (venv)
```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Основные ссылки
- Главная: `/`
- Треки: `/music/tracks/`
- Альбомы: `/music/albums/`
- Админка: `/admin/`
- API: `/api/`
- Swagger UI: `/api/docs/`
- OpenAPI JSON: `/api/schema/`
- ReDoc: `/api/redoc/`

## API
- GET /api/tracks/ — список, поиск (`search`), фильтры (`album__genres`, `artists`), сортировка (`ordering`)
- GET /api/albums/
- POST /api/playlists/ — создать плейлист (нужно войти), поле `track_ids`
- POST /api/tracks/{id}/toggle_favorite/ — в избранное/из избранного (нужно войти)

## База данных
- По умолчанию: SQLite (локально).
- В docker-compose: PostgreSQL. Для продакшна рекомендовано использовать Postgres; можно вынести настройки БД в переменные окружения.

## Соответствие критериям
- Аутентификация/авторизация (CustomUser, формы, админ-роль)
- Ядро: артисты, жанры, альбомы, треки, плейлисты, избранное
- Поиск/фильтрация/сортировка/пагинация в API и UI
- Админ-панель
- Логи (`django.log`)
- Тесты (`music/tests.py`)
- Swagger/OpenAPI (`/api/docs/`)
- Dockerfile + docker-compose
- CI (GitHub Actions)
- Нагрузочное тестирование (`k6/load.js`)

## Weekly Report шаблон
1. Выполненные задачи
2. Прогресс проекта (%)
3. Проблемы и решения
4. План на следующую неделю

## Развертывание
Готов Docker-образ (`gunicorn`). Для Render/Heroku задайте `SECRET_KEY`, `DEBUG=False`, переменные БД. Автодеплой можно настроить через GitHub Actions.
