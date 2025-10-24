from django.contrib import admin
from .models import CustomUser, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'bio')
    search_fields = ('user__username', 'user__email', 'avatar')
    readonly_fields = ()  # or ('avatar',) if you want it read-only

admin.site.register(CustomUser)
