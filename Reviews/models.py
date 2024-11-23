from django.db import models
from users .models import Customer
from Restaurants.models import Restaurant
from django.db.models import Avg, F
# Create your models here.

class ReviewManager(models.Manager):
    def calculate_average_rating(self, restaurant):
        reviews = self.filter(restaurant=restaurant)
        avg_rating = reviews.aggregate(
            avg_rating=Avg(
                (F('food_rating') + F('service_rating') + F('delivery_time_rating') + F('packaging_rating') + F('order_accuracy_rating')) / 5
            )
        )['avg_rating']
        return round(avg_rating, 2) if avg_rating else None

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    review_text = models.TextField()
    food_rating = models.IntegerField()
    service_rating = models.IntegerField()
    delivery_time_rating = models.IntegerField(blank=True, null=True)
    packaging_rating = models.IntegerField(blank=True, null=True)
    order_accuracy_rating = models.IntegerField(blank=True, null=True)
    review_img = models.ImageField(upload_to='review_images/', blank=True, null=True)
    likes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    dislikes = models.IntegerField(default=0)

    objects = ReviewManager()



class LikeDislike(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('customer', 'review')
