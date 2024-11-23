from django.contrib import admin
from.models import EatHubAdmin, Customer, RestaurantOwner
# Register your models here.

@admin.register(EatHubAdmin)
class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'email', 'is_staff', 'is_active', 'date_joined']

@admin.register(Customer)
class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'name', 'mobile_number', 'email', 'date_joined']

@admin.register(RestaurantOwner)
class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'name', 'mobile_number', 'email', 'date_joined']