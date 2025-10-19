from django.contrib import admin


from .models import SiteStats, Fundraiser, Pledge

admin.site.register(SiteStats)
admin.site.register(Fundraiser)
admin.site.register(Pledge)
