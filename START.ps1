# PowerShell скрипт для быстрого запуска проекта

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Запуск Movie Music Catalog" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "[1/3] Активация виртуального окружения..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "[2/3] Применение миграций БД..." -ForegroundColor Yellow
python manage.py migrate

Write-Host "[3/3] Запуск сервера разработки..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Сервер запущен!" -ForegroundColor Green
Write-Host "  Откройте: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

python manage.py runserver

