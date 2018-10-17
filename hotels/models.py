from django.db import models
from django.urls import reverse

# Create your models here.

class Hotel(models.Model):
    """Model definition for Hotel."""

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, default='123456789')
    email = models.EmailField(max_length=100, default='hotel_name@email.com')
    rating = models.PositiveIntegerField(default=3)

    def get_absolute_url(self):
        """Return absolute url for Hotel."""
        return reverse('hotels:hotel-detail', args=[str(self.pk)])

    def __str__(self):
        """Unicode representation of Hotel."""
        return self.name
