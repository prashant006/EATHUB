from django.urls import path
from . import views

urlpatterns = [   
    path("restaurant/home/", views.restaurant_home, name='restaurant_home'),
    path('restaurant/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurant/<int:id>/edit/', views.edit_restaurant_datail, name='edit_restaurant'),
    path('restaurant/<int:id>/delete/', views.delete_restaurant, name='delete_restaurant'),
    path('restaurant/<int:restaurant_id>/add_dish/', views.add_dish, name='add_dish'),
    path('restaurant/<int:restaurant_id>/view_order/', views.view_order, name='view_order'),
    path('restaurant/<int:restaurant_id>/dishes/', views.restaurant_dishes, name='restaurant_dishes'),
    path('restaurant/<int:restaurant_id>/dish/<int:dish_id>/delete/', views.delete_dish, name='delete_dish'),    
    path('restaurant/<int:restaurant_id>/dish/<int:dish_id>/update/', views.update_dish_info, name='update_dish'), 
    path('order/accept/<int:order_item_id>/', views.order_accept, name='order_accept'),
    path('order/ready/<int:order_item_id>/', views.order_ready, name='order_ready'),
    path('order/cancel/<int:order_item_id>/', views.order_cancel, name='order_cancel'),



    ]