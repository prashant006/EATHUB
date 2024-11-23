from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from.managers import CustomUserManager

class EatHubAdmin(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
 

class Customer(EatHubAdmin):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField(null=True, blank=True)
    profile = models.ImageField(upload_to='customer_profile_imagess/', blank=True, null=True)

    is_customer = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name
    

class RestaurantOwner(EatHubAdmin):    
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    profile = models.ImageField(upload_to='profile_images/', blank=True)
    
    is_restaurent = models.BooleanField(default=True)
    


    def __str__(self):
        return self.name