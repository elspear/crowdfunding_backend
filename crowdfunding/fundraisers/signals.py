from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db import transaction

from .models import Fundraiser, Pledge, SiteStats


def compute_site_stats():
    """
    Compute derived site-wide aggregates.
    Returns a dict keyed by SiteStats field names.
    """
    User = get_user_model()

    total_users = User.objects.count()
    total_fundraisers = Fundraiser.objects.count()

    # Count each fundraiser that has a pokemon set (each fundraiser counts once)
    total_pokemon_helped = Fundraiser.objects.exclude(pokemon="").count()

    total_pledges = Pledge.objects.count()
    total_amount_pledged = Pledge.objects.aggregate(total=Sum("amount"))["total"] or 0

    return {
        "total_users": total_users,
        "total_fundraisers": total_fundraisers,
        "total_pokemon_helped": total_pokemon_helped,
        "total_pledges": total_pledges,
        "total_amount_pledged": total_amount_pledged,
    }


def update_site_stats():
    """
    Compute and persist stats if any value changed.
    Uses transaction.on_commit to avoid saving inside an open transaction.
    """
    stats = SiteStats.get_stats()  # your classmethod
    values = compute_site_stats()

    changed = False
    for key, new_val in values.items():
        if getattr(stats, key, None) != new_val:
            setattr(stats, key, new_val)
            changed = True

    if not changed:
        return

    def _do_save():
        stats.save()

    transaction.on_commit(_do_save)


# Register receivers for the models which affect stats.
@receiver([post_save, post_delete], sender=get_user_model())
@receiver([post_save, post_delete], sender=Fundraiser)
@receiver([post_save, post_delete], sender=Pledge)
def _on_model_change(sender, instance, **kwargs):
    # Keep receiver cheap; delegate heavier work to update_site_stats.
    update_site_stats()