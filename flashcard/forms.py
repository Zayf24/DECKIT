from django import forms
from .models import Deck

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'theme']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Deck Name'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
        }
