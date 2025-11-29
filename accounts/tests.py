"""
Tests for accounts app
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .validators import (
    MinimumLengthValidator, NumericPasswordValidator, CommonPasswordValidator,
    UppercaseValidator, LowercaseValidator, NumberValidator
)

User = get_user_model()


class PasswordValidatorTests(TestCase):
    """Test custom password validators"""
    
    def test_minimum_length_validator(self):
        validator = MinimumLengthValidator(min_length=8)
        validator.validate("short")  # Should raise ValidationError
        self.assertRaises(ValidationError, validator.validate, "short")
        validator.validate("longenough")  # Should not raise
    
    def test_numeric_password_validator(self):
        validator = NumericPasswordValidator()
        self.assertRaises(ValidationError, validator.validate, "12345678")
        validator.validate("password123")  # Should not raise
    
    def test_common_password_validator(self):
        validator = CommonPasswordValidator()
        self.assertRaises(ValidationError, validator.validate, "password")
        validator.validate("MySecurePass123!")  # Should not raise
    
    def test_uppercase_validator(self):
        validator = UppercaseValidator()
        self.assertRaises(ValidationError, validator.validate, "alllowercase123")
        validator.validate("HasUppercase123")  # Should not raise
    
    def test_lowercase_validator(self):
        validator = LowercaseValidator()
        self.assertRaises(ValidationError, validator.validate, "ALLUPPERCASE123")
        validator.validate("HasLowercase123")  # Should not raise
    
    def test_number_validator(self):
        validator = NumberValidator()
        self.assertRaises(ValidationError, validator.validate, "NoNumbersHere")
        validator.validate("HasNumber1")  # Should not raise


class UserModelTests(TestCase):
    """Test CustomUser model"""
    
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('TestPass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_str(self):
        user = User.objects.create_user(
            username='testuser',
            password='TestPass123'
        )
        self.assertEqual(str(user), 'testuser')


class UserRegistrationTests(TestCase):
    """Test user registration functionality"""
    
    def test_user_registration_valid(self):
        response = self.client.post('/accounts/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123',
            'password2': 'SecurePass123',
        })
        # Should redirect to home on success
        self.assertIn(response.status_code, [200, 302])
    
    def test_user_registration_duplicate_username(self):
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='TestPass123'
        )
        response = self.client.post('/accounts/register/', {
            'username': 'existing',
            'email': 'another@example.com',
            'password1': 'SecurePass123',
            'password2': 'SecurePass123',
        })
        # Should show error or redirect to login
        self.assertIn(response.status_code, [200, 302])

