"""
Integration tests for API endpoints
"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from music.models import Artist, Genre, Album, Track
from movies.models import Movie, Genre as MovieGenre, Director, Actor

User = get_user_model()


class AuthAPITests(APITestCase):
    """Test authentication API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123',
            email='test@example.com'
        )
    
    def test_api_register(self):
        """Test user registration via API"""
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123',
            'password2': 'SecurePass123',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
    
    def test_api_login(self):
        """Test user login via API"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPass123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
    
    def test_api_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_api_logout(self):
        """Test user logout via API"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_logout_requires_auth(self):
        """Test logout requires authentication"""
        response = self.client.post('/api/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_api_user_info(self):
        """Test getting current user info"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')


class HealthCheckTests(APITestCase):
    """Test health check endpoints"""
    
    def test_health_check(self):
        """Test basic health check"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')
    
    def test_health_detailed(self):
        """Test detailed health check"""
        response = self.client.get('/api/health/detailed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('checks', response.data)
        self.assertIn('database', response.data['checks'])
    
    def test_health_ready(self):
        """Test readiness probe"""
        response = self.client.get('/api/health/ready/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_health_live(self):
        """Test liveness probe"""
        response = self.client.get('/api/health/live/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ErrorHandlingTests(APITestCase):
    """Test error handling"""
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/api/tracks/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
    
    def test_validation_error(self):
        """Test validation error handling"""
        response = self.client.post('/api/auth/register/', {
            'username': 'test',
            # Missing required fields
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class PaginationTests(APITestCase):
    """Test pagination functionality"""
    
    def setUp(self):
        # Create test data
        artist = Artist.objects.create(name="Test Artist")
        genre = Genre.objects.create(name="Rock")
        album = Album.objects.create(title="Test Album", artist=artist, release_year=2020)
        album.genres.add(genre)
        
        # Create multiple tracks for pagination
        for i in range(25):
            track = Track.objects.create(title=f"Track {i}", album=album, duration=180)
            track.artists.add(artist)
    
    def test_pagination_default_page_size(self):
        """Test default pagination"""
        response = self.client.get('/api/tracks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertEqual(response.data['count'], 25)
        self.assertEqual(len(response.data['results']), 20)  # Default page size
    
    def test_pagination_custom_page(self):
        """Test pagination with custom page"""
        response = self.client.get('/api/tracks/?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 5)  # Remaining items

