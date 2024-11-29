from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Profile


class LoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(max_length=80)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomRegisterForm(UserCreationForm):
    """Custom register form extending the default one with name and email"""
    first_name = forms.CharField(
        max_length=30, required=True, help_text='First name')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Last name')
    email = forms.EmailField(required=True, help_text='Email address')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def clean_email(self):
        """Validate email for uniqueness"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Invalid email address")
        return email


class UserEditForm(forms.ModelForm):
    """Form for updating a user's information"""
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']

    # make the email field mandatory
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        query = User.objects.filter(email=email).exclude(id=self.instance.id)

        if query.exists():
            raise forms.ValidationError("Invalid email address")
        return email


class ProfileEditForm(forms.ModelForm):
    """Form for editing a user's profile information"""
    class Meta:
        model = Profile
        fields = ['gender', 'phone', 'date_of_birth',
                  'home_address', 'delivery_address']
