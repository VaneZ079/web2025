from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ['cover_image', 'detail_image', 'average_rating']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'genres': forms.CheckboxSelectMultiple,
            'platforms': forms.CheckboxSelectMultiple,
        }
