from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Restaurants.models import Restaurant, RestaurantMenu
from users.models import Customer
from Reviews.models import Review
from.models import Cart, CartItem
from decimal import Decimal



# Create your views here.
@login_required(login_url='login')
def customer_home_page(request):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        restaurants = Restaurant.objects.all()
            
        return render(request, 'customer/home.html', {'restaurants':restaurants})
    else:
        return redirect('login')

@login_required(login_url='login')
def restaurant_detail(request, restaurant_id):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        # reviews = Review.objects.filter(restaurant=restaurant)
        dishes = RestaurantMenu.objects.filter(restaurent=restaurant)
        avg_rating = Review.objects.calculate_average_rating(restaurant)
        return render(request, 'customer/restaurant_detail.html', {'dishes':dishes, 'restaurant':restaurant, 'avg_rating':avg_rating})
    else:
        return redirect('login')
    

@login_required(login_url='login')
def add_to_cart(request, dish_id ):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        # breakpoint()
        dish = get_object_or_404(RestaurantMenu, id = dish_id )
        customer = Customer.objects.get(pk=request.user.id)
        #check or create for customer
        cart, created = Cart.objects.get_or_create(customer = customer, order=False)
        #cheack or create for dish in cart
        cart_item, created = CartItem.objects.get_or_create(dish = dish, customer = customer, cart = cart, defaults={'price': dish.price, 'quantity': 1})
        
        if not created:
            cart_item.quantity += 1
            cart_item.price = cart_item.quantity * dish.price
            cart_item.save()
        else:
            cart_item.price = dish.price

        cart.total_price = Decimal(cart.total_price) + dish.price
        cart.save()
        messages.success(request, f"{dish.dish_name} has been added to your cart.")
        return redirect('restaurant_detail', restaurant_id = dish.restaurent.id)
    else:
        return redirect('login')

def view_cart(request):
    customer = request.user.customer 
    cart = get_object_or_404(Cart, customer=customer, order=False)
    cart_items = CartItem.objects.filter(cart=cart)
    return render (request, 'customer/view_cart.html', {'cart': cart, 'cart_items': cart_items})

@login_required(login_url='login')    
def remove_cart_item(request,  item_id):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        cart_item = get_object_or_404(CartItem, id = item_id)
        cart = cart_item.cart 
        cart_item.delete()
        # cart.total_price = 0
        cart.total_price = Decimal(cart.total_price) - cart_item.dish.price * cart_item.quantity
        cart.save()
        messages.success(request, f"item has been removed successfully.")
        return redirect('view_cart')
    else:
        return redirect('login')


@login_required(login_url='login')    
def decrese_item_quantity(request,  item_id):
    
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        
        cart_item = get_object_or_404(CartItem, id = item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

            cart = cart_item.cart 
            cart.total_price = Decimal(cart.total_price) - cart_item.dish.price 
            cart.save()
            dish = cart_item.dish
            cart_item.price = cart_item.quantity * dish.price
            cart_item.save()
            messages.success(request, "cart update successfully!")
        else:
            messages.error(request, "Quantity cannot be less than 1.")
        return redirect('view_cart')
    else:
        return redirect('login')

@login_required(login_url='login')    
def increse_item_quantity(request,  item_id):
    
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        cart_item = get_object_or_404(CartItem, id = item_id)
        if cart_item.quantity < 10:
            cart_item.quantity += 1
            cart_item.save()

            cart = cart_item.cart 
            cart.total_price = Decimal(cart.total_price) + cart_item.dish.price 
            cart.save()
            dish = cart_item.dish
            cart_item.price = cart_item.quantity * dish.price
            cart_item.save()
            messages.success(request, "cart update successfully!")
        else:
            messages.error(request, "Quantity can't be more than 10")
        return redirect('view_cart')
    else:
        return redirect('login')
