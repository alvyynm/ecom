from django import forms


class LoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(max_length=80)
    password = forms.CharField(widget=forms.PasswordInput)
