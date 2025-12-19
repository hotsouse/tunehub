"""
Команда для быстрого создания суперпользователя (администратора)
Использование: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает суперпользователя (администратора) для доступа к админ-панели'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Имя пользователя (по умолчанию: admin)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email адрес (по умолчанию: admin@example.com)'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Пароль (если не указан, будет запрошен интерактивно)'
        )
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Не запрашивать интерактивный ввод (требует --password)'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        no_input = options['no_input']

        # Проверяем, существует ли уже пользователь
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Пользователь "{username}" уже существует!')
            )
            if not no_input:
                overwrite = input('Хотите изменить пароль? (y/n): ')
                if overwrite.lower() != 'y':
                    self.stdout.write(self.style.SUCCESS('Отменено.'))
                    return
                user = User.objects.get(username=username)
                if not password:
                    password = self._get_password()
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Пароль для пользователя "{username}" обновлен!')
                )
                self._print_info(username, password)
                return
            else:
                self.stdout.write(
                    self.style.ERROR('Пользователь уже существует. Используйте --no-input=false для изменения.')
                )
                return

        # Запрашиваем пароль, если не указан
        if not password:
            if no_input:
                self.stdout.write(
                    self.style.ERROR('Требуется указать --password при использовании --no-input')
                )
                return
            password = self._get_password()

        # Создаем суперпользователя
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Суперпользователь "{username}" успешно создан!')
            )
            self._print_info(username, password)
            
        except IntegrityError:
            self.stdout.write(
                self.style.ERROR(f'Ошибка: пользователь "{username}" уже существует!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании пользователя: {e}')
            )

    def _get_password(self):
        """Запрашивает пароль дважды для подтверждения"""
        while True:
            password = input('Введите пароль: ')
            if len(password) < 8:
                self.stdout.write(
                    self.style.WARNING('Пароль должен содержать минимум 8 символов!')
                )
                continue
            password_confirm = input('Подтвердите пароль: ')
            if password != password_confirm:
                self.stdout.write(
                    self.style.ERROR('Пароли не совпадают! Попробуйте снова.')
                )
                continue
            return password

    def _print_info(self, username, password):
        """Выводит информацию для входа"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('ИНФОРМАЦИЯ ДЛЯ ВХОДА:'))
        self.stdout.write('='*60)
        self.stdout.write(f'Имя пользователя: {username}')
        self.stdout.write(f'Пароль: {password}')
        self.stdout.write('\nАдмин-панель Django: http://127.0.0.1:8000/admin/')
        self.stdout.write('='*60 + '\n')

