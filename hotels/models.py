from django.db import models
from django.urls import reverse

# Create your models here.

class Hotel(models.Model):
    """Model definition for Hotel."""

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.TextField(default="Address")
    contact = models.CharField(max_length=100, default='123456789')
    email = models.EmailField(max_length=100, default='hotel_name@email.com')
    rating = models.PositiveIntegerField(default=3)

    def get_absolute_url(self):
        """Return absolute url for Hotel."""
        return reverse('hotels:hotel-detail', args=[str(self.pk)])

    def __str__(self):
        """Unicode representation of Hotel."""
        return str(self.name) + '(' + str(self.location) + ')'
class Room(models.Model):
    """Model definition for Room."""

    OCCUPANCY_CHOICES = [
        ("SINGLE", "SINGLE"),
        ("DOUBLE", "DOUBLE"),
    ]
    TYPE_CHOICES = [
        ("A/C(Air Conditioned)", "A/C(Air Conditioned)"),
        ("Non A/C(Non Air Conditioned)", "Non A/C(Non Air Conditioned)"),
    ]

    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE)
    type_name = models.CharField(max_length=100, default="Deluxe")
    occupancy = models.CharField(max_length=50, choices=OCCUPANCY_CHOICES , default="SINGLE")
    room_type = models.CharField(max_length=50, choices=TYPE_CHOICES , default="Non A/C(Non Air Conditioned)")
    maximum = models.PositiveIntegerField(default=10)
    available = models.PositiveIntegerField(default=10)
    cost = models.PositiveIntegerField(default=1000)

    def get_absolute_url(self):
        """Return absolute url for Room."""
        return reverse('hotels:room-detail', args=[str(self.hotel.pk), str(self.pk)])

    def __str__(self):
        """Unicode representation of Room."""
        return str(self.hotel) + ' ' + self.type_name + ' ' + self.occupancy + ' ' + self.room_type

class Booking(models.Model):
    """Model definition for Booking."""
    
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    room = models.ForeignKey('hotels.Room', on_delete=models.CASCADE)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    num_rooms = models.PositiveIntegerField()
    amount = models.PositiveIntegerField() 

    def __str__(self):
        """Unicode representation of Booking."""
        return str(self.room.pk) + ' ' + str(self.num_rooms)