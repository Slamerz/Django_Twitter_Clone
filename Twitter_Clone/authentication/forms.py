from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password'
        ]
