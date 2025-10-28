from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def ensure_profile_and_sync_username(sender, instance, created, **kwargs):
    """
    Ensure a Profile exists for every User. On creation, create the Profile
    and seed profile.username from user.username (if that field exists).
    On subsequent saves, ensure a Profile exists and keep profile.username
    in sync using a QuerySet update for efficiency.
    """
    # Create profile if missing; when creating, try to set username and avatar directly
    if created:
        # If Profile has a username field, set it at creation to avoid an extra save
        try:
            # Get avatar from instance if it was passed during signup
            avatar = getattr(instance, '_avatar', None)
            Profile.objects.create(
                user=instance, 
                username=instance.username,
                avatar=avatar or ''  # Use empty string if no avatar provided
            )
        except TypeError:
            # Profile model doesn't accept username in constructor (field may not exist)
            Profile.objects.create(user=instance)
    else:
        # Defensive: ensure profile exists (get_or_create is cheap for most workloads)
        Profile.objects.get_or_create(user=instance)

    # If the Profile model actually defines a 'username' field, sync it from the User.
    # Use a QuerySet update to avoid loading the Profile instance and triggering
    # signal recursion or additional save handlers.
    has_username_field = any(f.name == "username" for f in Profile._meta.get_fields())
    if has_username_field and getattr(instance, "username", None):
        Profile.objects.filter(user=instance).update(username=instance.username)