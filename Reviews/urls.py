from django.urls import path
from . import views
from .views import like_review, dislike_review

urlpatterns = [
    
    path('submit_review/<int:restaurant_id>/', views.submit_review, name='submit_review'),
    path('show_review/<int:restaurant_id>/', views.Show_reviews, name='show_review'),
    path('like/<int:review_id>/', like_review, name='like_review'),
    path('dislike/<int:review_id>/', dislike_review, name='dislike_review'),
]
