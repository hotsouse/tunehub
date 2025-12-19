from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from .models import CustomUser

def register(request):
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже вошли в систему.')
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Регистрация успешна! Добро пожаловать, {user.username}!')
                # Перенаправляем в админ-панель, если пользователь - администратор
                if user.is_staff:
                    return redirect('admin_panel')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Ошибка при регистрации: {str(e)}')
        else:
            # Показываем ошибки формы
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже вошли в систему.')
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Добро пожаловать, {username}!')
                    # Перенаправляем в админ-панель, если пользователь - администратор
                    if user.is_staff:
                        return redirect('admin_panel')
                    return redirect('home')
                else:
                    messages.error(request, 'Ваш аккаунт деактивирован. Обратитесь к администратору.')
            else:
                # Проверяем, существует ли пользователь
                try:
                    user_check = CustomUser.objects.get(username=username)
                    messages.error(request, 'Неверный пароль. Проверьте правильность ввода.')
                except CustomUser.DoesNotExist:
                    messages.error(request, f'Пользователь "{username}" не найден. Проверьте имя пользователя или зарегистрируйтесь.')
        else:
            # Показываем ошибки формы
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f'{field}: {error}')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'favorite_movies': request.user.favorite_movies.all()[:5],
        'favorite_music': request.user.favorite_music.all()[:5],
    }
    return render(request, 'accounts/profile.html', context)