from django.contrib import admin
from .models import User, Manager, Customer

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(User, UserAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Customer, CustomerAdmin)
