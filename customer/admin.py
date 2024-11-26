from django.contrib import admin

from.models import Cart, CartItem, Order, OrderItem
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order', 'total_price']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'dish', 'customer', 'cart', 'price', 'total_item', 'quantity']
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order_date', 'is_delivered', 'delivery_address', 'total_price', 'payment_status']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'item', 'item_price', 'quantity']
    