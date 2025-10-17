from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import os
from datetime import datetime
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-super-secret-jwt-key-change-this-in-production'

# Папка для данных
DATA_DIR = 'data'
MOVIES_FILE = os.path.join(DATA_DIR, 'movies.json')
MUSIC_FILE = os.path.join(DATA_DIR, 'music.json')
FAVORITES_FILE = os.path.join(DATA_DIR, 'favorites.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

# Создаем папку для данных если ее нет
os.makedirs(DATA_DIR, exist_ok=True)

# Инициализация файлов данных
def init_data():
    if not os.path.exists(MOVIES_FILE):
        sample_movies = [
            {
                'id': 1,
                'title': 'Inception',
                'year': 2010,
                'genre': 'Sci-Fi',
                'rating': 8.8,
                'description': 'A thief who steals corporate secrets through dream-sharing technology.',
                'director': 'Christopher Nolan',
                'duration': 148
            }
        ]
        with open(MOVIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(sample_movies, f, ensure_ascii=False, indent=2)
    
    if not os.path.exists(MUSIC_FILE):
        sample_music = [
            {
                'id': 1,
                'title': 'Bohemian Rhapsody',
                'artist': 'Queen',
                'album': 'A Night at the Opera',
                'year': 1975,
                'genre': 'Rock',
                'duration': 354
            }
        ]
        with open(MUSIC_FILE, 'w', encoding='utf-8') as f:
            json.dump(sample_music, f, ensure_ascii=False, indent=2)
    
    if not os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            json.dump({'movies': [], 'music': []}, f, ensure_ascii=False, indent=2)
    
    # Инициализация пользователей
    if not os.path.exists(USERS_FILE):
        sample_users = [
            {
                'id': 1,
                'username': 'admin',
                'password': generate_password_hash('admin123'),
                'email': 'admin@example.com',
                'role': 'admin',
                'created_at': datetime.utcnow().isoformat()
            }
        ]
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sample_users, f, ensure_ascii=False, indent=2)

# Чтение данных
def read_movies():
    with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_music():
    with open(MUSIC_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_favorites():
    with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_users():
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Запись данных
def write_movies(data):
    with open(MOVIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_music(data):
    with open(MUSIC_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_favorites(data):
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_users(data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Поиск и сортировка
def search_items(items, query, fields):
    if not query:
        return items
    query = query.lower()
    results = []
    for item in items:
        for field in fields:
            if field in item and query in str(item[field]).lower():
                results.append(item)
                break
    return results

def sort_items(items, sort_by, order='asc'):
    if not sort_by:
        return items
    
    reverse = (order == 'desc')
    
    try:
        if sort_by in ['year', 'rating', 'duration']:
            # Преобразуем в числа для правильной сортировки
            return sorted(items, key=lambda x: float(x.get(sort_by, 0)), reverse=reverse)
        elif sort_by == 'artist':
            return sorted(items, key=lambda x: str(x.get('artist', '')).lower(), reverse=reverse)
        elif sort_by == 'title':
            return sorted(items, key=lambda x: str(x.get('title', '')).lower(), reverse=reverse)
        elif sort_by == 'album':
            return sorted(items, key=lambda x: str(x.get('album', '')).lower(), reverse=reverse)
        else:
            return sorted(items, key=lambda x: str(x.get(sort_by, '')).lower(), reverse=reverse)
    except (ValueError, TypeError):
        # Если возникает ошибка, возвращаем исходный список
        return items

# Декоратор для проверки JWT токена
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            token = token.split(' ')[1]  # Убираем 'Bearer '
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = next((user for user in read_users() if user['id'] == data['user_id']), None)
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token verification failed!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# Декоратор для проверки роли администратора
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = next((user for user in read_users() if user['id'] == data['user_id']), None)
            
            if not current_user or current_user.get('role') != 'admin':
                return jsonify({'message': 'Admin access required!'}), 403
                
        except Exception as e:
            return jsonify({'message': 'Token verification failed!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# ==================== ЭНДПОИНТЫ АВТОРИЗАЦИИ ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            return jsonify({'message': 'Username, password and email are required!'}), 400
        
        users = read_users()
        
        # Проверяем, существует ли пользователь
        if any(user['username'] == data['username'] for user in users):
            return jsonify({'message': 'Username already exists!'}), 400
        
        if any(user['email'] == data['email'] for user in users):
            return jsonify({'message': 'Email already exists!'}), 400
        
        new_user = {
            'id': max([user['id'] for user in users], default=0) + 1,
            'username': data['username'],
            'password': generate_password_hash(data['password']),
            'email': data['email'],
            'role': 'user',
            'created_at': datetime.utcnow().isoformat()
        }
        
        users.append(new_user)
        write_users(users)
        
        # Создаем токен для автоматического входа после регистрации
        token = jwt.encode({
            'user_id': new_user['id'],
            'username': new_user['username'],
            'exp': datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'User created successfully!',
            'token': token,
            'user': {
                'id': new_user['id'],
                'username': new_user['username'],
                'email': new_user['email'],
                'role': new_user['role']
            }
        }), 201
        
    except Exception as e:
        return jsonify({'message': 'Server error during registration'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username and password are required!'}), 400
        
        users = read_users()
        user = next((u for u in users if u['username'] == data['username']), None)
        
        if user and check_password_hash(user['password'], data['password']):
            # Создаем JWT токен
            token = jwt.encode({
                'user_id': user['id'],
                'username': user['username'],
                'exp': datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'message': 'Login successful!',
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200
        
        return jsonify({'message': 'Invalid credentials!'}), 401
        
    except Exception as e:
        return jsonify({'message': 'Server error during login'}), 500

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({
        'id': current_user['id'],
        'username': current_user['username'],
        'email': current_user['email'],
        'role': current_user['role']
    }), 200

@app.route('/api/auth/users', methods=['GET'])
@admin_required
def get_all_users(current_user):
    users = read_users()
    # Не возвращаем пароли
    safe_users = [
        {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'created_at': user.get('created_at', '')
        }
        for user in users
    ]
    return jsonify(safe_users), 200

# ==================== СУЩЕСТВУЮЩИЕ ЭНДПОИНТЫ ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies')
def movies():
    movies_data = read_movies()
    query = request.args.get('search', '')
    sort_by = request.args.get('sort', '')
    order = request.args.get('order', 'asc')
    
    # Поиск
    if query:
        movies_data = search_items(movies_data, query, ['title', 'genre', 'director', 'description'])
    
    # Сортировка
    if sort_by:
        movies_data = sort_items(movies_data, sort_by, order)
    
    favorites_data = read_favorites()
    
    return render_template('movies.html', 
                         movies=movies_data, 
                         search_query=query, 
                         sort_by=sort_by, 
                         order=order,
                         favorites=favorites_data['movies'])

@app.route('/music')
def music():
    music_data = read_music()
    query = request.args.get('search', '')
    sort_by = request.args.get('sort', '')
    order = request.args.get('order', 'asc')
    genre_filter = request.args.get('genre', '')
    year_filter = request.args.get('year', '')
    
    # Поиск
    if query:
        music_data = search_items(music_data, query, ['title', 'artist', 'album', 'genre'])
    
    # Фильтр по жанру
    if genre_filter:
        music_data = [music for music in music_data if music.get('genre', '').lower() == genre_filter.lower()]
    
    # Фильтр по году
    if year_filter:
        music_data = [music for music in music_data if str(music.get('year', '')) == year_filter]
    
    # Сортировка
    if sort_by:
        music_data = sort_items(music_data, sort_by, order)
    
    # Получаем уникальные жанры для фильтра
    all_music = read_music()
    unique_genres = sorted(set(music.get('genre', '') for music in all_music if music.get('genre')))
    
    # Исправленная сортировка годов - преобразуем в int для правильной сортировки
    unique_years = sorted(
        set(int(music.get('year', 0)) for music in all_music if music.get('year') and str(music.get('year')).isdigit()),
        reverse=True
    )
    
    favorites_data = read_favorites()
    
    return render_template('music.html', 
                         music=music_data, 
                         search_query=query,
                         sort_by=sort_by, 
                         order=order,
                         genre_filter=genre_filter,
                         year_filter=year_filter,
                         genres=unique_genres,
                         years=unique_years,
                         favorites=favorites_data['music'])

@app.route('/favorites')
def favorites():
    favorites_data = read_favorites()
    movies_data = read_movies()
    music_data = read_music()
    
    # Получаем полные данные об избранных элементах
    favorite_movies = [movie for movie in movies_data if movie['id'] in favorites_data['movies']]
    favorite_music = [music for music in music_data if music['id'] in favorites_data['music']]
    
    return render_template('favorites.html', movies=favorite_movies, music=favorite_music)

@app.route('/add_to_favorites/<item_type>/<int:item_id>')
def add_to_favorites(item_type, item_id):
    favorites_data = read_favorites()
    
    if item_type == 'movie' and item_id not in favorites_data['movies']:
        favorites_data['movies'].append(item_id)
        write_favorites(favorites_data)
    elif item_type == 'music' and item_id not in favorites_data['music']:
        favorites_data['music'].append(item_id)
        write_favorites(favorites_data)
    
    return redirect(request.referrer or url_for('index'))

@app.route('/remove_from_favorites/<item_type>/<int:item_id>')
def remove_from_favorites(item_type, item_id):
    favorites_data = read_favorites()
    
    if item_type == 'movie' and item_id in favorites_data['movies']:
        favorites_data['movies'].remove(item_id)
        write_favorites(favorites_data)
    elif item_type == 'music' and item_id in favorites_data['music']:
        favorites_data['music'].remove(item_id)
        write_favorites(favorites_data)
    
    return redirect(request.referrer or url_for('index'))

@app.route('/admin')
def admin():
    movies_data = read_movies()
    music_data = read_music()
    return render_template('admin.html', movies=movies_data, music=music_data)

@app.route('/add/movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movies_data = read_movies()
        new_movie = {
            'id': max([movie['id'] for movie in movies_data], default=0) + 1,
            'title': request.form['title'],
            'year': int(request.form['year']),
            'genre': request.form['genre'],
            'rating': float(request.form['rating']),
            'description': request.form['description'],
            'director': request.form.get('director', ''),
            'duration': int(request.form.get('duration', 0))
        }
        movies_data.append(new_movie)
        write_movies(movies_data)
        return redirect(url_for('movies'))
    return render_template('add_edit_item.html', item_type='movie', item=None)

@app.route('/add/music', methods=['GET', 'POST'])
def add_music():
    if request.method == 'POST':
        music_data = read_music()
        new_music = {
            'id': max([music['id'] for music in music_data], default=0) + 1,
            'title': request.form['title'],
            'artist': request.form['artist'],
            'album': request.form['album'],
            'year': int(request.form['year']),
            'genre': request.form['genre'],
            'duration': int(request.form.get('duration', 0))
        }
        music_data.append(new_music)
        write_music(music_data)
        return redirect(url_for('music'))
    return render_template('add_edit_item.html', item_type='music', item=None)

@app.route('/edit/movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movies_data = read_movies()
    movie = next((m for m in movies_data if m['id'] == movie_id), None)
    
    if not movie:
        return redirect(url_for('movies'))
    
    if request.method == 'POST':
        movie.update({
            'title': request.form['title'],
            'year': int(request.form['year']),
            'genre': request.form['genre'],
            'rating': float(request.form['rating']),
            'description': request.form['description'],
            'director': request.form.get('director', ''),
            'duration': int(request.form.get('duration', 0))
        })
        write_movies(movies_data)
        return redirect(url_for('movies'))
    
    return render_template('add_edit_item.html', item_type='movie', item=movie)

@app.route('/edit/music/<int:music_id>', methods=['GET', 'POST'])
def edit_music(music_id):
    music_data = read_music()
    music = next((m for m in music_data if m['id'] == music_id), None)
    
    if not music:
        return redirect(url_for('music'))
    
    if request.method == 'POST':
        music.update({
            'title': request.form['title'],
            'artist': request.form['artist'],
            'album': request.form['album'],
            'year': int(request.form['year']),
            'genre': request.form['genre'],
            'duration': int(request.form.get('duration', 0))
        })
        write_music(music_data)
        return redirect(url_for('music'))
    
    return render_template('add_edit_item.html', item_type='music', item=music)

@app.route('/delete/movie/<int:movie_id>')
def delete_movie(movie_id):
    movies_data = read_movies()
    movies_data = [movie for movie in movies_data if movie['id'] != movie_id]
    write_movies(movies_data)
    
    # Удаляем из избранного
    favorites_data = read_favorites()
    if movie_id in favorites_data['movies']:
        favorites_data['movies'].remove(movie_id)
        write_favorites(favorites_data)
    
    return redirect(url_for('admin'))

@app.route('/delete/music/<int:music_id>')
def delete_music(music_id):
    music_data = read_music()
    music_data = [music for music in music_data if music['id'] != music_id]
    write_music(music_data)
    
    # Удаляем из избранного
    favorites_data = read_favorites()
    if music_id in favorites_data['music']:
        favorites_data['music'].remove(music_id)
        write_favorites(favorites_data)
    
    return redirect(url_for('admin'))

# Защищенные API эндпоинты
@app.route('/api/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': f'Hello {current_user["username"]}! This is protected data.'}), 200

@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def admin_stats(current_user):
    movies = read_movies()
    music = read_music()
    users = read_users()
    
    stats = {
        'total_movies': len(movies),
        'total_music': len(music),
        'total_users': len(users),
        'admin_users': len([u for u in users if u.get('role') == 'admin']),
        'regular_users': len([u for u in users if u.get('role') == 'user'])
    }
    
    return jsonify(stats), 200

if __name__ == '__main__':
    init_data()
    app.run(debug=True)