from django import forms
from .models import Movie, Genre, Director, Actor, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_year', 'duration', 'genres', 'directors', 'actors']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название фильма'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание фильма'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900', 'max': '2030'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Длительность в минутах'}),
            'genres': forms.CheckboxSelectMultiple(),
            'directors': forms.CheckboxSelectMultiple(),
            'actors': forms.CheckboxSelectMultiple(),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 11)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш отзыв (необязательно)'}),
        }