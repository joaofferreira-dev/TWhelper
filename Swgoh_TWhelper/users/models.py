
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
"""
Class that extends to default User class of Django, for adding extra fields\
"""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Full_defense_mode = models.BooleanField(default=False)
    Game_name = models.CharField(max_length=22, default='None')
    Discord_id = models.CharField(max_length=20, default='None')


"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""
