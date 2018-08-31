from django.contrib import admin
from .models import Hotel

# Register your models here.

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact', 'email', 'amount')

admin.site.register(Hotel, HotelAdmin)
