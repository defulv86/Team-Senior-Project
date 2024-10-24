# Import necessary modules for signal handling and user model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Signal to create a UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a UserProfile for the new user
        user_profile = UserProfile.objects.create(user=instance)
        
        # Set permission level based on whether the user is a superuser
        if instance.is_superuser:
            user_profile.permission_level = 2  # Permission level for superusers
        else:
            user_profile.permission_level = 1  # Default permission level for regular users
        
        # Save the UserProfile with the assigned permission level
        user_profile.save()

# Signal to save and update the UserProfile when the User instance is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save() 

