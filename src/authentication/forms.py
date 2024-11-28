from django import forms


class LoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(max_length=80)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    """Register form"""
    username = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
