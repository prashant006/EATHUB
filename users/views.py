from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .forms import CustomerSignUpForm, EditProfileForm, CustomLoginForm, RestaurantOwnerSignUpForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from Restaurants.models import Restaurant, RestaurantMenu
from Reviews.models import Review
from django.core.mail import send_mail
from django.conf import settings




# Create your views here.




def base_page(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'customer') and request.user.customer.is_customer:
            return redirect('customer_home')
        elif hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
            return redirect('restaurant_home')
        if request.user.is_superuser:
            return redirect('admin_home')
    else:
        restaurants = Restaurant.objects.all()
        return render(request, 'guest_home.html', {'restaurants':restaurants})


def user_logIn(request):

    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomLoginForm(request=request, data=request.POST)
            if form.is_valid():
                email = form.cleaned_data["username"]
                password = form.cleaned_data["password"]

                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
                        return redirect('customer_home') 
                    elif hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
                        return redirect('restaurant_home')
                    if request.user.is_superuser:
                        return redirect('admin_home')
                              
        else:
            form = CustomLoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        if hasattr(request.user, 'customer') and request.user.customer.is_customer:
            return redirect('customer_home') 
        elif hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
            return redirect('restaurant_home')
        if request.user.is_superuser:
            return redirect('admin_home')



def user_logout(request):
    logout(request)
    return redirect('login')

def admin_home_page(request):
    if request.user.is_authenticated:        
        return render(request, 'admin/home.html')
    else:
        return redirect('login')
    

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_home')
    else:
        form = CustomerSignUpForm()
    return render(request, 'customer/signup.html', {'form':form})


def restaurant_owner_signup(request):
    if request.method == 'POST':
        form =RestaurantOwnerSignUpForm (request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_home')
    else:
        form = RestaurantOwnerSignUpForm()
    return render(request, 'restaurant/signup.html', {'form':form})

@login_required(login_url='login')
def  restaurant_home_page(request):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance = request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'pofile update !!!')
        else:
            form = EditProfileForm(instance = request.user)
        return render(request, 'restaurant/home.html', {'form':form})
    else:
        return redirect('login')
    


def update_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'password update successfully')
            return redirect('customer_home')
        
    else:
        form = PasswordChangeForm(user = request.user)
    return render(request, 'updatepass.html', {'form':form})
  
# if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = EditProfileForm(request.POST, instance = request.user)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'pofile update !!!')
#         else:
#             form = EditProfileForm(instance = request.user)
#         return render(request, 'customer/home.html', {'form':form})
#     else:
#         return redirect('login')

