from django.contrib import admin

from.models import Restaurant,RestaurantMenu
# Register your models here.

@admin.register(Restaurant)
class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'contact_info', 'avg_rating']

@admin.register(RestaurantMenu)
class RestaurantMenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurent', 'dish_name', 'price']