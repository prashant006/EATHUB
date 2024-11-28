from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Restaurants.models import Restaurant, RestaurantMenu
from users.models import Customer
from Reviews.models import Review
from.models import Cart, CartItem, Order, OrderItem
from decimal import Decimal
import stripe
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime



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
            cart = get_object_or_404(Cart, id = cart_id, customer = request.user.customer)
            cart_items = CartItem.objects.filter(cart = cart)

            session_id = request.GET.get('session_id')
            if session_id:
                session = stripe.checkout.Session.retrieve(session_id)
                payment_intent_id = session.payment_intent
            
            if not cart_items.exists():
                    messages.error(request, "Your cart is empty!")
                    return redirect('view_cart')
            order = Order.objects.create(
                    customer=request.user.customer,
                    delivery_address= request.user.customer.address,
                    total_price = cart.total_price
            )
            order.payment_intent_id = payment_intent_id
            order.payment_status = 'SUCCESS'
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
                genrate_order_recipt(order_item.order)
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

@login_required(login_url='login')
def cancel_order(request, order_item_id):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        # breakpoint()
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        order = order_item.order
        refund = stripe.Refund.create(
            payment_intent = order.payment_intent_id,
            amount = int(order_item.item_price)*100
        )
        if refund.status == 'succeeded':
            if order_item.order_status == 'PLACED':
                order_item.order_status = 'CANCELLED'
                order_item.save()

                subject = f"Order status"
                message = f"Dear {order_item.customer} your order has {order_item.order_status} and your refund of {order_item.item_price} has been initiate to your account \n Thank you team EATHUB"
                send_mail(subject, message, 'nickypatle006@gmail.com', {order_item.customer.email})

            messages.success(request, f"Cancel item successfully.")
        else:
            messages.warning(request, f"refund failed.")

        return redirect('order_detail',order_id = order_item.order.id)
    else:
        return redirect('login')
    


# payment method
stripe.publishable_key = 'pk_test_51QOIQEATEkbiPlGMwykLADnJq7SiqEN28O5TEr39iRfgK9i47ax8laiZBTZmehSE5aZ1nC894VuelLIAJJovTgrb00G2viL3Ly'
stripe.api_key = 'sk_test_51QOIQEATEkbiPlGMrF6bMNOZt0Xqa3JLCdPxs7Z3WqeXIh6U68BtKiDkMeGNNkLjCjCJBVYThG97jz84FKsbo2CK00N9q04J8k'
def checkout_session(request, cart_id):
    cart = get_object_or_404(Cart, id = cart_id)

    DOMAIN = 'http://127.0.0.1:8000' 
    success_url = f"{DOMAIN}/place_order/{cart_id}/?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{DOMAIN}/payment_failed/"

    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items=[
            {
                'price_data' : {
                    'currency': 'inr', 
                    'product_data':  {'name': 'order'},
                    'unit_amount': int(cart.total_price)*100
                },
                'quantity': 1
            },
        ],
        mode='payment',
        success_url = success_url,
        cancel_url = cancel_url,
    )
    return redirect(session.url, code = 303)

def payment_failed(request):
    messages.warning(request, f"Payment failed.")
    return redirect('view_cart')

# message
#  
def genrate_order_recipt(order):
    customer = order.customer 
    order_items = OrderItem.objects.filter(order=order) 

    order_details = []
    for item in order_items:
        order_details.append({
            'restaurant': item.restaurant.name,
            'item_name': item.item_name,
            'item_price': item.item_price,
            'quantity': item.quantity,
            'item_image': item.item_image.url if item.item_image else None,
            'order_status': item.order_status,
        })

    html_string = render_to_string('customer/order_receipt.html', {
        'customer': customer,
        'order_id': order.id,
        'order_details': order_details,
        'total_price': order.total_price
    })

    # Generate the PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    pdf_file = ContentFile(pdf)
    order.order_receipt.save(f"order_receipt_{customer.name}.pdf", pdf_file)

    subject = "Order summary"
    message = f"Dear {customer.name}, your order has been placed successfully."

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[customer.email],
    )
    email.attach(f"order_receipt_{customer.name}.pdf", pdf, 'application/pdf')
    email.send()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="order_receipt.pdf"'
    return response



