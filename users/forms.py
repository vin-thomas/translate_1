from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"create username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"enter email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"create password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"repeat password"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"enter first name"}), max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"enter last name"}), max_length=30, help_text='Required. Enter your last name.')

    class Meta:
        model = User
        fields = [
            'username',
            'email', 
            'first_name',
            'last_name',
            'password1', 
            'password2', 
        ]