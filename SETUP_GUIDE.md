# Setup Guide

Подробное руководство по установке и развертыванию проекта Movie Music Catalog.

## Требования

- Python 3.11+
- PostgreSQL 13+ (для production) или SQLite (для разработки)
- Docker и Docker Compose (опционально, для контейнеризации)
- Git

## Вариант 1: Локальная установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd movie_music_catalog
```

### 2. Создание виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка базы данных

#### SQLite (для разработки)

Просто выполните миграции:

```bash
python manage.py migrate
```

#### PostgreSQL (для production)

1. Установите PostgreSQL и создайте базу данных:

```bash
createdb catalog_db
```

2. Настройте переменные окружения:

**Windows (PowerShell):**
```powershell
$env:DB_NAME="catalog_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
```

**Linux/Mac:**
```bash
export DB_NAME=catalog_db
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

3. Выполните миграции:

```bash
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Загрузка тестовых данных (опционально)

```bash
python manage.py load_sample_music
python manage.py load_sample_movies
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: `http://localhost:8000`

## Вариант 2: Docker

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd movie_music_catalog
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=catalog_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```

**Важно**: Для production измените `SECRET_KEY` на случайный ключ!

### 3. Сборка и запуск контейнеров

```bash
docker-compose up --build
```

### 4. Создание суперпользователя

В отдельном терминале:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Доступ к приложению

- Приложение: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/api/docs/`
- Admin панель: `http://localhost:8000/admin/`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (логин: admin/admin)

## Настройка для Production

### 1. Переменные окружения

Создайте `.env` файл или настройте переменные окружения:

```env
DEBUG=False
SECRET_KEY=<generate-random-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=catalog_db
DB_USER=postgres
DB_PASSWORD=<strong-password>
DB_HOST=db
DB_PORT=5432
```

### 2. Генерация SECRET_KEY

```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Сборка статических файлов

```bash
python manage.py collectstatic --noinput
```

### 4. Миграции

```bash
python manage.py migrate
```

### 5. Запуск с Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 catalog.wsgi:application
```

### 6. Настройка веб-сервера (Nginx)

Пример конфигурации Nginx:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/media/;
    }
}
```

## Развертывание на Render

### 1. Подготовка

1. Убедитесь, что ваш код в GitHub репозитории
2. Подключите репозиторий к Render

### 2. Настройка сервисов

#### Web Service
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command**: `gunicorn catalog.wsgi:application`
- **Environment Variables**:
  - `SECRET_KEY`: случайный ключ
  - `DEBUG`: `False`
  - `ALLOWED_HOSTS`: ваш домен
  - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: из PostgreSQL сервиса

#### PostgreSQL Database
- Создайте отдельный PostgreSQL сервис
- Скопируйте connection string в переменные окружения Web Service

### 3. Миграции

Настройте автоматические миграции в Build Command:

```bash
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

## Развертывание на Heroku

### 1. Установка Heroku CLI

Следуйте инструкциям на [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### 2. Создание приложения

```bash
heroku create your-app-name
```

### 3. Добавление PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 4. Настройка переменных окружения

```bash
heroku config:set SECRET_KEY=$(python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

### 5. Деплой

```bash
git push heroku main
```

### 6. Миграции и создание суперпользователя

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Мониторинг

### Prometheus

Метрики доступны по адресу: `/metrics/`

### Grafana

1. Откройте `http://localhost:3000` (для Docker)
2. Войдите с логином: `admin` / `admin`
3. Настройте источник данных Prometheus: `http://prometheus:9090`
4. Импортируйте готовые дашборды

### Health Checks

- Basic: `/api/health/`
- Detailed: `/api/health/detailed/`
- Readiness: `/api/health/ready/`
- Liveness: `/api/health/live/`

## Troubleshooting

### Проблема: "Database connection failed"

**Решение**: Проверьте переменные окружения для БД и убедитесь, что PostgreSQL запущен.

### Проблема: "Static files not found"

**Решение**: Выполните `python manage.py collectstatic`

### Проблема: "CSRF verification failed"

**Решение**: Убедитесь, что используете HTTPS в production или добавьте домен в `CSRF_TRUSTED_ORIGINS`

### Проблема: "SECRET_KEY not set"

**Решение**: Установите переменную окружения `SECRET_KEY`

## Дополнительная информация

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Docker Documentation](https://docs.docker.com/)
- [Render Documentation](https://render.com/docs)
- [Heroku Django Guide](https://devcenter.heroku.com/articles/django-app-configuration)

