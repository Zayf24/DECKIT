from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    phone=forms.CharField(max_length=10, required=True)
    date_of_birth=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    image=forms.ImageField(required=False)
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['name','username', 'email','phone','date_of_birth','password1', 'password2','image']