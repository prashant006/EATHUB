from django.urls import path

from customer import views


urlpatterns = [  
    path("customer_home/", views.customer_home_page, name='customer_home'),
    path("customer_home/<int:restaurant_id>/restaurant_detail", views.restaurant_detail, name='restaurant_detail'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart', views.view_cart, name='view_cart'),
    path('remove_cart_item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('decrese_item_quantity/<int:item_id>/', views.decrese_item_quantity, name='decrese_item_quantity'),
    path('increse_item_quantity/<int:item_id>/', views.increse_item_quantity, name='increse_item_quantity'),


    
]