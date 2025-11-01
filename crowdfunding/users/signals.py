from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def ensure_profile_and_sync_username(sender, instance, created, **kwargs):
    """
    Ensure a Profile exists for every User and sync profile data.
    """
    try:
        with transaction.atomic():
            if created:
                print(f"Creating profile for user {instance.username}")
                
                # Get the temporary attributes with proper fallbacks
                avatar = getattr(instance, "_avatar", "") or ""
                location = getattr(instance, "_location", "") or ""
                
                print(f"Creating profile with: avatar={avatar}, location={location}")
                
                try:
                    profile = Profile.objects.create(
                        user=instance,
                        username=instance.username,
                        avatar=avatar,
                        location=location,
                    )
                    print(f"Created profile successfully: {profile.location}")
                    
                    # Verify the profile was created with correct data
                    profile.refresh_from_db()
                    print(f"Profile after refresh: location={profile.location}")
                    
                except Exception as e:
                    print(f"Error in profile creation: {str(e)}")
                    raise
            else:
                # For existing users, ensure profile exists and sync username
                try:
                    profile, created = Profile.objects.get_or_create(user=instance)
                    if created:
                        print(f"Created profile for existing user: {instance.username}")
                    
                    # Keep Profile.username in sync
                    if hasattr(Profile, 'username') and profile.username != instance.username:
                        profile.username = instance.username
                        profile.save()
                        print(f"Synced username for profile: {profile.username}")
                        
                except Exception as e:
                    print(f"Error in profile sync: {str(e)}")
                    raise

    except Exception as e:
        print(f"Critical error in signal handler: {str(e)}")
        # In production, you might want to log this instead of raising
        raise