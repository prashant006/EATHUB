from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddDishForm, AddRestaurantForm
from .models import Restaurant,RestaurantMenu
from customer.models import Order, OrderItem
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.

@login_required(login_url='login')
def restaurant_home(request):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        data = Restaurant.objects.filter(owner=request.user)
        return render(request, 'restaurant/home.html', {'restaurants':data})

    else:
        return redirect('login')
    
@login_required(login_url='login')
def add_restaurant(request):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        if request.method == 'POST':
            form = AddRestaurantForm(request.POST, request.FILES,)
            if form.is_valid():
                rest = form.save(commit=False)
                rest.owner = request.user.restaurantowner
                rest.save()
                return redirect('restaurant_home')
        else:
            form = AddRestaurantForm()
        return render(request, 'restaurant/add_restaurant.html', {'form':form})
    else:
        return redirect('login')
    

@login_required(login_url='login')
def delete_restaurant(request, id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        data = Restaurant.objects.get(pk = id)
        data.delete()
        return redirect('restaurant_home')
    else:
        return redirect('login')
    
    
@login_required(login_url='login')
def edit_restaurant_datail(request, id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        if request.method == 'POST':
            pi = Restaurant.objects.get(pk = id)
            form = AddRestaurantForm(request.POST, request.FILES, instance = pi)
            if form.is_valid():
                form.save()
                return redirect('restaurant_home')
            else:
                return render(request, 'restaurant/edit_restaurant.html',{'form': form, 'error': 'Enter valid data'})
        else:
            pi = Restaurant.objects.get(pk = id)
            form = AddRestaurantForm(instance = pi)
        return render(request, 'restaurant/edit_restaurant.html',{'form': form, })
    else:
        return redirect ('login')
    

@login_required(login_url='login')
def restaurant_dishes(request, restaurant_id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        restaurant = Restaurant.objects.get(id=restaurant_id, owner=request.user.restaurantowner)            
        dishes = RestaurantMenu.objects.filter(restaurent=restaurant)
        return render(request, 'restaurant/restaurant_dishes.html', {'restaurant': restaurant, 'dishes': dishes})
    else:
        return redirect('login') 

    

@login_required(login_url='login')
def add_dish(request, restaurant_id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=request.user.restaurantowner)
        if request.method == 'POST':
            form = AddDishForm(request.POST, request.FILES)
            if form.is_valid():
                dish = form.save(commit=False)
                dish.restaurent = restaurant
                dish.save()
                return redirect('restaurant_dishes', restaurant_id=restaurant.id)
            else:
                return render(request, 'restaurant/add_dish.html', {'form': form, 'restaurant': restaurant, 'error': 'Form is not valid'})

        else:
            form = AddDishForm()
        return render(request, 'restaurant/add_dish.html', {'form': form, 'restaurant': restaurant})
    else:
        return redirect('login')
    
    
@login_required(login_url='login')    
def delete_dish(request, dish_id, restaurant_id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        dish = get_object_or_404(RestaurantMenu, id=dish_id, restaurent__id=restaurant_id, restaurent__owner=request.user.restaurantowner)
        if request.method == 'POST':  
            dish.delete()
            messages.success(request, f"The dish '{dish.dish_name}' has been deleted successfully.")
            return redirect('restaurant_dishes', restaurant_id=restaurant_id)
        else:
            messages.error(request, "Invalid request.")
            return redirect('restaurant_dishes', restaurant_id=restaurant_id)
    else:
        return redirect('login')
    

@login_required(login_url='login')    
def update_dish_info(request, dish_id, restaurant_id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        dish = get_object_or_404(RestaurantMenu, id=dish_id, restaurent__id=restaurant_id, restaurent__owner=request.user.restaurantowner)

        if request.method == 'POST':
            form = AddDishForm(request.POST, request.FILES, instance=dish)

            if form.is_valid():
                form.save()
                return redirect('restaurant_dishes', restaurant_id=restaurant_id)

            else:
                return render(request, 'restaurant/update_dish.html',{'form': form, 'error': 'Enter valid data'})
        else:
            form = AddDishForm(request.FILES,instance=dish)
        return render(request, 'restaurant/update_dish.html',{'form': form, 'dish':dish})
    else:
        return redirect ('login')


@login_required(login_url='login')
def view_order(request, restaurant_id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        order_item = OrderItem.objects.filter(restaurant = restaurant)
        return render(request, 'restaurant/view_order.html', {'restaurant':restaurant, 'order_item':order_item})
    else:
        return redirect('login')


@login_required(login_url='login')
def order_accept(request, order_item_id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        if order_item.order_status == 'PLACED':
            order_item.order_status = 'ACCEPT'
            order_item.save()
        return redirect('view_order', restaurant_id= order_item.restaurant.id)
    else:
        return redirect('login')
    
@login_required(login_url='login')
def order_ready(request, order_item_id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        if order_item.order_status == 'ACCEPT':
            order_item.order_status = 'ON_THE_WAY'
            order_item.save()
        return redirect('view_order', restaurant_id= order_item.restaurant.id)
    else:
        return redirect('login')
    
@login_required(login_url='login')
def order_cancel(request, order_item_id):
    if hasattr(request.user, 'restaurantowner') and request.user.restaurantowner.is_restaurent:
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        if order_item.order_status == 'PLACED':
            order_item.order_status = 'CANCELLED'
            order_item.save()
            
            subject = f"Order status"
            message = f"Dear {order_item.customer} your order has {order_item.order_status} and your refund of {order_item.item_price} has been initiate to your account \n Thank you team EATHUB"
            send_mail(subject, message, 'nickypatle006@gmail.com', {order_item.customer.email})
        return redirect('view_order', restaurant_id= order_item.restaurant.id)
    else:
        return redirect('login')