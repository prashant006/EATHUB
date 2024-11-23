from django.contrib import admin

from.models import Cart, CartItem
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order', 'total_price']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'dish', 'customer', 'cart', 'price', 'total_item', 'quantity']
