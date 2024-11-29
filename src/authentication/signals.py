from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # create a new profile when a user is created
        Profile.objects.create(user=instance)
    else:
        # save the profile when a user is updated
        instance.profile.save()
