from django.urls import path
from django.contrib.auth import views as auth_views
from users import views


urlpatterns = [
    path("", views.base_page, name='basepage' ),
    path("login/", views.user_logIn, name='login'),
    path("logout/", views.user_logout, name='logout'),
    path("admin_home/", views.admin_home_page, name='admin_home'),
    path("customer_signup/", views.customer_signup, name='customer_signup'),    
    path("restaurant_signup/", views.restaurant_owner_signup, name='restaurant_signup'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='reset_password/password_reset_form.html'),
         name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='reset_password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='reset_password/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='reset_password/password_reset_complete.html'),
         name='password_reset_complete'),
         



    
    
]