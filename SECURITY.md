# Security Implementation

Документ описывает меры безопасности, реализованные в проекте Movie Music Catalog.

## Защита паролей

### Хеширование паролей
Django использует **PBKDF2** (Password-Based Key Derivation Function 2) алгоритм для хеширования паролей. Это обеспечивает:
- Безопасное хранение паролей (пароли никогда не хранятся в открытом виде)
- Защиту от атак по словарю и перебору
- Использование соли для каждого пароля

### Валидация паролей
Реализованы кастомные валидаторы паролей в `accounts/validators.py`:
- **MinimumLengthValidator**: Минимум 8 символов
- **NumericPasswordValidator**: Пароль не может быть полностью числовым
- **CommonPasswordValidator**: Проверка на распространенные пароли
- **UppercaseValidator**: Минимум одна заглавная буква
- **LowercaseValidator**: Минимум одна строчная буква
- **NumberValidator**: Минимум одна цифра

## Защита от атак

### CSRF (Cross-Site Request Forgery)
- Django автоматически защищает все формы от CSRF атак через middleware `CsrfViewMiddleware`
- CSRF токены добавляются во все формы через шаблонный тег `{% csrf_token %}`
- В production режиме (`DEBUG=False`) CSRF cookies помечаются как `Secure`

### XSS (Cross-Site Scripting)
- Django автоматически экранирует все переменные в шаблонах
- Используется `X-XSS-Protection` заголовок
- Защита от XSS через `SECURE_BROWSER_XSS_FILTER = True`

### SQL Injection
- Django ORM защищает от SQL инъекций через параметризованные запросы
- Все запросы к БД проходят через ORM, прямые SQL запросы не используются
- Использование параметризованных запросов в raw SQL (если необходимо)

### Clickjacking Protection
- Защита через `X-Frame-Options: DENY` заголовок
- Настройка: `X_FRAME_OPTIONS = 'DENY'`

## Аутентификация и авторизация

### Аутентификация
- Session-based аутентификация (Django Sessions)
- Basic Authentication для API (опционально)
- Проверка прав доступа через декораторы и permissions

### Авторизация
- Разделение ролей: обычные пользователи и администраторы (`is_staff`, `is_superuser`)
- Проверка прав доступа в API через `permission_classes`
- Логирование действий пользователей (логирование входа/выхода)

## Production Security Settings

В production режиме (`DEBUG=False`) активируются дополнительные настройки безопасности:

```python
SECURE_SSL_REDIRECT = True  # Принудительное перенаправление на HTTPS
SESSION_COOKIE_SECURE = True  # Cookies только по HTTPS
CSRF_COOKIE_SECURE = True  # CSRF cookies только по HTTPS
SECURE_BROWSER_XSS_FILTER = True  # Защита от XSS
SECURE_CONTENT_TYPE_NOSNIFF = True  # Защита от MIME sniffing
X_FRAME_OPTIONS = 'DENY'  # Защита от clickjacking
SECURE_HSTS_SECONDS = 31536000  # HTTP Strict Transport Security
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## Секретные ключи

### SECRET_KEY
- **Никогда не коммитьте SECRET_KEY в репозиторий!**
- Используйте переменные окружения: `SECRET_KEY = os.environ.get('SECRET_KEY')`
- Для production генерируйте новый SECRET_KEY: `python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### Database Credentials
- Используйте переменные окружения для учетных данных БД
- Не храните пароли БД в коде или в файлах конфигурации

## Логирование и мониторинг

### Логирование безопасности
- Логирование неудачных попыток входа
- Логирование критических операций
- Структурированное логирование для анализа

### Мониторинг
- Prometheus метрики для мониторинга
- Health checks для отслеживания состояния системы
- Логи ошибок для анализа инцидентов

## API Security

### API Authentication
- Session Authentication для веб-интерфейса
- Basic Authentication для API (с ограничениями)
- Защита чувствительных endpoints через `permission_classes`

### CORS
- В production настройте `CORS_ALLOWED_ORIGINS` вместо `CORS_ALLOW_ALL_ORIGINS = True`
- Ограничьте доступ только с разрешенных доменов

### Rate Limiting
- Рекомендуется добавить rate limiting для API endpoints (например, через `django-ratelimit`)

## Best Practices

1. **Регулярно обновляйте зависимости**: `pip list --outdated`
2. **Используйте только HTTPS в production**
3. **Проводите security audits**: `bandit -r .`
4. **Проверяйте уязвимости**: `pip audit` (Python 3.11+)
5. **Используйте сильные пароли**: минимально 8 символов, буквы + цифры
6. **Храните секреты в переменных окружения**
7. **Регулярно делайте бэкапы БД**
8. **Мониторьте логи на подозрительную активность**

## Обнаружение уязвимостей

Если вы обнаружили уязвимость безопасности, пожалуйста:
1. **НЕ** создавайте публичный issue
2. Свяжитесь с командой разработки приватно
3. Опишите проблему детально
4. Дождитесь ответа перед публичным разглашением

## Инструменты безопасности

- **Bandit**: статический анализатор безопасности Python кода
- **pip audit**: проверка зависимостей на уязвимости
- **OWASP Dependency-Check**: сканирование зависимостей
- **django-security**: дополнительные проверки безопасности Django

## Дополнительные ресурсы

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security](https://python.readthedocs.io/en/latest/library/security.html)

