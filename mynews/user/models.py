from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Example: Phone number
    date_of_birth = models.DateField(blank=True, null=True)  # Example: Date of birth
    trusted_users = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='trusted_by') #Or related_name='trusted_users'

   
    def __str__(self):
        return self.username