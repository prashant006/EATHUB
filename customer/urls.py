from django.urls import path

from customer import views


urlpatterns = [  
    path("customer_home/", views.customer_home_page, name='customer_home'),
    path("customer_home/<int:restaurant_id>/restaurant_detail", views.restaurant_detail, name='restaurant_detail'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove_cart_item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('decrese_item_quantity/<int:item_id>/', views.decrese_item_quantity, name='decrese_item_quantity'),
    path('increse_item_quantity/<int:item_id>/', views.increse_item_quantity, name='increse_item_quantity'),
    path('place_order/<int:cart_id>/', views.place_order, name='place_order'),
    path('view_order/', views.view_order, name='view_order'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel_order/<int:order_item_id>/', views.cancel_order, name='cancel_order'),
    path('checkout_session/<int:cart_id>/', views.checkout_session, name='checkout_session'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),   
]