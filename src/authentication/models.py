from django.db import models
from django.conf import settings


class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'
        NULL = 'none'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_complete = models.BooleanField(default=False)
    phone = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=Gender.choices)
    date_of_birth = models.DateField(null=True, blank=True)
    home_address = models.CharField(max_length=250, null=True, blank=True)
    delivery_address = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
