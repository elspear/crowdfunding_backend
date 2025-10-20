from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count #sum & count needed for signals

class SiteStats(models.Model):
    total_fundraisers = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    total_pledges = models.IntegerField(default=0)
    total_amount_pledged = models.IntegerField(default=0)
    total_pokemon_helped = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Site Statistics - Last Updated: {self.last_updated}"

    @classmethod
    def get_stats(cls):
        stats, created = cls.objects.get_or_create(pk=1)
        return stats

    class Meta:
        verbose_name_plural = "Site Statistics"

class Fundraiser(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pokemon = models.CharField(max_length=100)
    goal = models.IntegerField()
    items_needed = models.CharField(max_length=200) #list 
    image = models.URLField()
    is_open = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(
        get_user_model(),
        related_name='owned_fundraisers',
        on_delete=models.CASCADE
    )

class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)    
    anonymous = models.BooleanField()
    fundraiser = models.ForeignKey(
        'Fundraiser',
        related_name='pledges',
        on_delete=models.CASCADE
    )
    supporter = models.ForeignKey(
        get_user_model(),
        related_name='pledges',
        on_delete=models.CASCADE
    )

