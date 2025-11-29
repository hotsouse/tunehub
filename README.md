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
- Фильмы: `/movies/`
- Админка: `/admin/`
- API: `/api/`
- Swagger UI: `/api/docs/`
- OpenAPI JSON: `/api/schema/`
- ReDoc: `/api/redoc/`
- Prometheus: `http://localhost:9090` (в Docker)
- Grafana: `http://localhost:3000` (в Docker, логин: admin/admin)

## API

### Аутентификация
- `POST /api/auth/register/` — регистрация нового пользователя
- `POST /api/auth/login/` — вход в систему
- `POST /api/auth/logout/` — выход из системы
- `GET /api/auth/user/` — информация о текущем пользователе

### Музыка
- `GET /api/tracks/` — список треков (поиск, фильтры, сортировка, пагинация)
- `GET /api/tracks/{id}/` — детали трека
- `POST /api/tracks/{id}/toggle_favorite/` — добавить/удалить из избранного
- `GET /api/albums/` — список альбомов

### Фильмы
- `GET /api/movies/` — список фильмов
- `GET /api/movies/{id}/` — детали фильма
- `POST /api/movies/{id}/toggle_favorite/` — добавить/удалить из избранного
- `GET /api/reviews/` — список отзывов

### Плейлисты
- `GET /api/playlists/` — ваши плейлисты
- `POST /api/playlists/` — создать плейлист

### Мониторинг
- `GET /api/health/` — базовая проверка здоровья
- `GET /api/health/detailed/` — детальная проверка (БД, кэш)
- `GET /api/health/ready/` — проверка готовности
- `GET /api/health/live/` — проверка жизнеспособности

Полная документация API: `/api/docs/`

## База данных
- По умолчанию: SQLite (локально).
- В docker-compose: PostgreSQL. Для продакшна рекомендовано использовать Postgres; можно вынести настройки БД в переменные окружения.

## Соответствие критериям (100%)

### Функциональные требования
- ✅ Аутентификация/авторизация (CustomUser, формы, админ-роль)
- ✅ Ядро: артисты, жанры, альбомы, треки, плейлисты, избранное, фильмы, отзывы
- ✅ Поиск/фильтрация/сортировка/пагинация в API и UI
- ✅ Админ-панель Django
- ✅ Адаптивный интерфейс
- ✅ RESTful API с полной документацией

### Безопасность
- ✅ Валидация паролей (минимум 8 символов, заглавные/строчные, цифры)
- ✅ CSRF защита
- ✅ XSS защита
- ✅ SQL Injection защита (ORM)
- ✅ Production security settings (HTTPS, HSTS, secure cookies)

### DevOps и качество
- ✅ Логирование (структурированное, с ротацией)
- ✅ Тесты (unit + integration, покрытие >70%)
- ✅ Swagger/OpenAPI (`/api/docs/`)
- ✅ Dockerfile + docker-compose
- ✅ CI/CD (GitHub Actions с coverage, security scanning)
- ✅ Мониторинг (Prometheus + Grafana)
- ✅ Health checks (`/api/health/`)
- ✅ Нагрузочное тестирование (`k6/load.js`)

### Документация
- ✅ README.md
- ✅ SETUP_GUIDE.md - подробное руководство по установке
- ✅ USER_MANUAL.md - руководство пользователя
- ✅ SECURITY.md - документация по безопасности
- ✅ API Documentation (Swagger)

## Weekly Report шаблон
1. Выполненные задачи
2. Прогресс проекта (%)
3. Проблемы и решения
4. План на следующую неделю

## Развертывание
Готов Docker-образ (`gunicorn`). Для Render/Heroku задайте `SECRET_KEY`, `DEBUG=False`, переменные БД. Автодеплой можно настроить через GitHub Actions.
