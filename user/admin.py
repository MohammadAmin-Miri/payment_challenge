from django.contrib import admin

from .models import CustomUser, State, City, Address


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone',
        'email',
        'first_name',
        'last_name',
        'date_joined',
        'phone_verified',
        'email_verified'
    )
    
    
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state_id')
    
    
@admin.register(Address)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'state_id', 'city_id', 'postal_code', 'description')

