from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Region(models.Model):
    """US States for geographic regions"""
    name = models.CharField(max_length=100)  # e.g., "Georgia"
    code = models.CharField(max_length=2, unique=True)  # e.g., "GA"
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        ordering = ['name']

class UserProfile(models.Model):
    """Extended user profile with location data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.region if self.region else 'No region'}"

# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
