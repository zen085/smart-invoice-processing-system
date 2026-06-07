from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )

class LoginForm(AuthenticationForm):
    pass
