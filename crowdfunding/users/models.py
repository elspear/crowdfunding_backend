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
    username = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    bio = models.TextField(blank=True)
    # Store a selected avatar identifier (frontend hosts the avatar images).
    # This can be a filename, a key, or a URL depending on how the frontend organizes avatars.
    avatar = models.CharField(max_length=200, blank=True, default="")
    location = models.CharField(max_length=100, blank=True, default="")

    # profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user and not self.username:
            self.username = self.user.username
        super().save(*args, **kwargs)

    

    def __str__(self):
        return f"{self.user.username}'s profile"