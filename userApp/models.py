from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class RoleChoices(models.TextChoices):
    CUSTOMER = 'customer', 'Customer'
    VENDOR = 'vendor', 'Vendor'
    ADMIN = 'admin', 'Admin'
    
class Role(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    address = models.TextField()
    roles = models.ManyToManyField(Role, blank=True, related_name="profiles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = UserProfile.objects.create(user=instance)
            profile.roles.add(RoleChoices.CUSTOMER)
            


