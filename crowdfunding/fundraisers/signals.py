from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Sum
from .models import Fundraiser, Pledge, SiteStats

def update_site_stats():
    stats = SiteStats.get_stats()
    User = get_user_model()
    
    # Update user count
    stats.total_users = User.objects.count()
    
    # Update fundraiser counts
    stats.total_fundraisers = Fundraiser.objects.count()
    
    # Count total Pokemon helped (all fundraisers)
    stats.total_pokemon_helped = Fundraiser.objects.count()
    
    # Update pledge statistics
    stats.total_pledges = Pledge.objects.count()
    total_pledged = Pledge.objects.aggregate(Sum('amount'))['amount__sum']
    stats.total_amount_pledged = total_pledged if total_pledged else 0
    
    stats.save()

@receiver([post_save, post_delete], sender=get_user_model())
@receiver([post_save, post_delete], sender=Fundraiser)
@receiver([post_save, post_delete], sender=Pledge)
def update_stats_on_change(sender, **kwargs):
    update_site_stats()
