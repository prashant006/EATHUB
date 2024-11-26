from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Restaurants.models import Restaurant, RestaurantMenu
from users.models import Customer
from Reviews.models import Review
from.models import Cart, CartItem, Order, OrderItem
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

# @login_required(login_url='login')
# def view_cart(request):
#     if hasattr(request.user, 'customer') and request.user.customer.is_customer:  
#         customer = request.user.customer 
        
#         cart = get_object_or_404(Cart, customer=customer, order=False)
#         cart_items = CartItem.objects.filter(cart=cart)
#         return render (request, 'customer/view_cart.html', {'cart': cart, 'cart_items': cart_items})
#     else:
#         return redirect('login')

@login_required(login_url='login')
def view_cart(request):
    # Check if the user is a customer
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        customer = request.user.customer

        # Get or create the cart for the customer
        cart, created = Cart.objects.get_or_create(customer=customer, order=False)

        # Get all items in the cart
        cart_items = CartItem.objects.filter(cart=cart)

        # Render the cart page
        return render(request, 'customer/view_cart.html', {'cart': cart, 'cart_items': cart_items})
    else:
        # Redirect to login if the user is not a customer
        return redirect('login')

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

@login_required(login_url='login')  
def place_order(request, cart_id):
    # breakpoint()
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        if request.method == 'POST' :  
            cart = get_object_or_404(Cart, id = cart_id, customer = request.user.customer)
            cart_items = CartItem.objects.filter(cart = cart)
            

            if not cart_items.exists():
                    messages.error(request, "Your cart is empty!")
                    return redirect('view_cart')
            order = Order.objects.create(
                    customer=request.user.customer,
                    delivery_address= request.user.customer.address,
                    total_price = cart.total_price
            )
            order.save()
            
            for item in cart_items: 
                order_item = OrderItem.objects.create(
                        customer = request.user.customer,
                        restaurant = item.dish.restaurent,
                        order  = order,
                        item = item,
                        item_price = item.price,
                        quantity = item.quantity, 
                        item_name = item.dish.dish_name,       
                )
                order_item.item_image = item.dish.dish_image
                order_item.save()

            cart.order = True
            cart.save()
            if cart.order == True:
                cart_items.delete()
            messages.success(request, f"Order placed successfull successfully.")
        return redirect('customer_home', )
    else:
        return redirect('login')

@login_required(login_url='login')
def view_order(request):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer) 
        Order_Item = OrderItem.objects.filter(customer = customer)
        return render(request, 'customer/view_order.html', {'orders': orders, 'Order_Item':Order_Item})
    else:
        return redirect('login')
    
from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def order_detail(request, order_id):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        return render(request, 'customer/order_detail.html', {'order_items': order_items, 'order': order})
    else:
        return redirect('login')




