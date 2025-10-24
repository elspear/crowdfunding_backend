from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('trainer', 'Trainer'),
        ('pokemon_center', 'Pokemon Center'),
        ('safari_park', 'Safari Park')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='trainer')
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True)
    avatar = models.CharField(max_length=200, blank=True, default="")

    def save(self, *args, **kwargs):
        if self.user and not self.username:
            self.username = self.user.username
            super().save(*args, **kwargs)

    

    def __str__(self):
        return f"{self.user.username}'s profile"