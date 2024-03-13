from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"create username"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"create password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"repeat password"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"enter first name"}), max_length=30, required=True, help_text='Required. Enter your first name.')
    # last_name = forms.CharField(widget=forms.TextInput(), max_length=30, required=True, help_text='Required. Enter your last name.')

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'password1', 
            'password2', 
        ]

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'enter username', 'id': 'id_username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'enter password',
            'id': 'id_password',
        }
))