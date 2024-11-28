from django.db import models
from users.models import Customer
from Restaurants.models import RestaurantMenu, Restaurant
# Create your models here.

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)

class CartItem(models.Model):
    dish = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_item = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('REFUNDED', 'Refunded'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    delivery_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_intent_id = models.CharField(max_length=250, blank=True, null=True)
    order_receipt = models.FileField(upload_to='order_recipt_pdf/', blank=True, null=True)
    
class OrderItem(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PLACED', 'Placed'),
        ('ACCEPT', 'Accept'),
        ('ON_THE_WAY', 'On_the_way'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(CartItem, on_delete=models.SET_NULL, null=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    item_image = models.ImageField(upload_to='order_item_images/', blank=True, null=True)
    item_name = models.CharField(max_length=100, default='item')
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='PLACED')

