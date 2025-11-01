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
    Also consume temporary attributes set on the user instance (e.g. _avatar, _location)
    that the signup serializer may have set.
    """
    if created:
        print(f"Creating profile for user {instance.username}")  # Debug log
        print(f"User _avatar: {getattr(instance, '_avatar', 'not set')}")  # Debug log
        print(f"User _location: {getattr(instance, '_location', 'not set')}")  # Debug log
        
        # Consume temporary attributes set by serializer
        avatar = getattr(instance, "_avatar", None)
        location = getattr(instance, "_location", None)
        print(f"Signal received location: {location}")  # Debug log
        
        # Only use empty string if the values are None
        avatar = "" if avatar is None else avatar
        location = "" if location is None else location

        try:
            profile = Profile.objects.create(
                user=instance,
                username=getattr(instance, "username", "") or "",
                avatar=avatar,
                location=location,
            )
            print(f"Created profile with location: {profile.location}")  # Debug log
        except TypeError:
            # Fallback if Profile constructor signature differs
            profile = Profile.objects.create(user=instance)
            if hasattr(profile, "username"):
                profile.username = getattr(instance, "username", "") or ""
            profile.avatar = avatar
            profile.location = location
            profile.save()
    else:
        # Ensure profile exists for existing users
        Profile.objects.get_or_create(user=instance)

    # Keep Profile.username in sync if the field exists
    has_username_field = any(f.name == "username" for f in Profile._meta.get_fields())
    if has_username_field and getattr(instance, "username", None):
        Profile.objects.filter(user=instance).update(username=instance.username)