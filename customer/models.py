from django.db import models
from users.models import Customer
from Restaurants.models import RestaurantMenu, Restaurant
# Create your models here.

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

class CartItem(models.Model):
    dish = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_item = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('proccessing', 'proccessing'),         
#         ('ordered', 'Ordered'),        
#         ('dispatch', 'dispatch'),         
#         ('delivered', 'Delivered'),     
#         ('cancelled', 'Cancelled'),     
#     ]
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     # dish = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
#     cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proccessing')
#     ordered_at = models.DateTimeField(auto_now_add=True) 
#     shipped_at = models.DateTimeField(auto_now_add=True) 
#     delivered_at = models.DateTimeField(auto_now_add=True)  
#     cancelled_at = models.DateTimeField(auto_now_add=True)  