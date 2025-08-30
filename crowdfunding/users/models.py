from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('trainer', 'Trainer'),
        ('pokemon_center', 'Pokemon Center'),
        ('safari_park', 'Safari Park')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='trainer')
    def __str__(self):
        return self.username