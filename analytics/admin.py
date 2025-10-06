from django.contrib import admin
from .models import Region, UserProfile

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'latitude', 'longitude']
    search_fields = ['name', 'code']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'region']
    list_filter = ['region']
    search_fields = ['user__username']
