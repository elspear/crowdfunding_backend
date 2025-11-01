from django.contrib import admin
from .models import CustomUser, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'bio', 'location')
    search_fields = ('user__username', 'user__email', 'avatar', 'location')
    readonly_fields = ()  # or ('avatar',) if you want it read-only

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email', 'role')