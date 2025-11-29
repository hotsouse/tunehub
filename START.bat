@echo off
echo ========================================
echo   Запуск Movie Music Catalog
echo ========================================
echo.

echo [1/3] Активация виртуального окружения...
call venv\Scripts\activate.bat

echo [2/3] Применение миграций БД...
python manage.py migrate

echo [3/3] Запуск сервера разработки...
echo.
echo ========================================
echo   Сервер запущен!
echo   Откройте: http://127.0.0.1:8000
echo ========================================
echo.
python manage.py runserver

pause

