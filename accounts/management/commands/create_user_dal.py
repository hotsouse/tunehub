"""
Команда для создания пользователя 'dal' с правами администратора
Использование: python manage.py create_user_dal
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает пользователя "dal" с правами администратора'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='dal123456',
            help='Пароль для пользователя (по умолчанию: dal123456)'
        )

    def handle(self, *args, **options):
        username = 'dal'
        password = options['password']
        email = 'dal@example.com'

        # Проверяем, существует ли уже пользователь
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            self.stdout.write(
                self.style.WARNING(f'Пользователь "{username}" уже существует!')
            )
            
            # Обновляем пароль и права
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            if email:
                user.email = email
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Пароль и права доступа для пользователя "{username}" обновлены!')
            )
        else:
            # Создаем нового пользователя
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.is_staff = True
                user.is_superuser = True
                user.is_active = True
                user.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Пользователь "{username}" успешно создан!')
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка: пользователь "{username}" уже существует!')
                )
                return
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка при создании пользователя: {e}')
                )
                return

        # Выводим информацию для входа
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('ИНФОРМАЦИЯ ДЛЯ ВХОДА:'))
        self.stdout.write('='*60)
        self.stdout.write(f'Имя пользователя: {username}')
        self.stdout.write(f'Пароль: {password}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Права администратора: Да (is_staff=True, is_superuser=True)')
        self.stdout.write('\nАдмин-панель: http://127.0.0.1:8000/admin-panel/')
        self.stdout.write('='*60 + '\n')

