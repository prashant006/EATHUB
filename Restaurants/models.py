from typing import Iterable
from django.db import models
from users.models import RestaurantOwner, Customer

# Create your models here.



class Restaurant(models.Model):
    CUISINE_CHOICES = [('Italian', 'Italian'), ('Chinese', 'Chinese'), ('Indian', 'Indian')]

    owner = models.ForeignKey(RestaurantOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    location = models.TextField(max_length=50)
    cuisine_type = models.CharField(max_length=50, choices=CUISINE_CHOICES)
    open_at = models.TimeField()
    close_at = models.TimeField()
    contact_info = models.CharField(max_length=100)
    restaurant_img = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    avg_rating = models.FloatField(default=0.0)

    

    def __str__(self):
        return self.name
    

    
class RestaurantMenu(models.Model):
    restaurent = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=50)
    discription = models.TextField(max_length=500)
    dish_image = models.ImageField(upload_to='dish_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

