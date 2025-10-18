from django import forms
from .models import Album, Track, Artist, Genre, Playlist


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'release_year', 'description', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название альбома'}),
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900', 'max': '2030'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание альбома'}),
            'genres': forms.CheckboxSelectMultiple(),
        }


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'album', 'duration', 'artists']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название трека'}),
            'album': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Длительность в секундах'}),
            'artists': forms.CheckboxSelectMultiple(),
        }


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название плейлиста'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Описание плейлиста'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }