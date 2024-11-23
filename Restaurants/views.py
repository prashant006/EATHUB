from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddDishForm, AddRestaurantForm
from .models import Restaurant,RestaurantMenu
from django.contrib import messages
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

