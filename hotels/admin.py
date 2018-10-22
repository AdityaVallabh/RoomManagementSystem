from django.contrib import admin
from .models import Hotel, Room, Booking

# Register your models here.
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'address', 'contact', 'email', 'rating')

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return self.readonly_fields + ('name', 'location')

    def get_queryset(self, request):
        qs = super(HotelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.manager.hotel.pk)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'type_name','occupancy','room_type','maximum','available','cost')

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return self.readonly_fields + ('hotel',)

    def get_queryset(self, request):
        qs = super(RoomAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(hotel=request.user.manager.hotel)

    def save_model(self, request, obj, form, change):
        obj.hotel = request.user.manager.hotel
        super(RoomAdmin, self).save_model(request, obj, form, change)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'begin_time', 'end_time' ,'room', 'num_rooms', 'amount']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return self.readonly_fields + ('customer', 'room')

    def get_queryset(self, request):
        qs = super(BookingAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(room__hotel=request.user.manager.hotel)
