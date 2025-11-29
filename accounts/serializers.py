"""
Serializers for user accounts
"""
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user information
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'profile_picture', 'bio', 'date_joined', 'is_staff']
        read_only_fields = ['id', 'date_joined', 'is_staff']

