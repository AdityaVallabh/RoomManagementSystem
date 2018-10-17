from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

class Manager(models.Model):
    """Model definition for Manager."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE)

    def __str__(self):
        """Unicode representation of Manager."""
        return self.user.username

class Customer(models.Model):
    """Model definition for Customer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        """Unicode representation of Customer."""
        return self.user.username


