from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_ensure_profile(sender, instance, created, **kwargs):
    """
    Ensure there is a Profile for every User and try to keep profile.username
    in sync with the User.username (if Profile has such a field).
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)

    # If Profile has a username field, ensure it's synced from the User
    try:
        profile = instance.profile  # uses related_name='profile'
        # Only set when the profile.username is empty and User.username is present
        if getattr(profile, "username", None) in (None, "") and getattr(instance, "username", None):
            profile.username = instance.username
            profile.save(update_fields=["username"])
    except Profile.DoesNotExist:
        # get_or_create above should have created the profile; ignore otherwise
        pass