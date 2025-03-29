from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import CUser

class CUserCreationForm(UserCreationForm):
    username = PhoneNumberField(region='IR', widget=forms.TextInput(attrs={'placeholder': 'e.g. +989123456789'}))
    
    class Meta:
        model = CUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')