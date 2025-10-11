# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture', 'bio']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'bio']

# movies/forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# music/forms.py
from django import forms
from .models import Playlist

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }