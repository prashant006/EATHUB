from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from users.models import  Customer
from Restaurants.models import Restaurant
from .models import Review, LikeDislike
from django.contrib import messages
# Create your views here.



@login_required(login_url='login')
def submit_review(request, restaurant_id):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES)
            
            if form.is_valid():
                # breakpoint()
                review = form.save(commit=False)
                review.restaurant = restaurant
                review.customer = request.user.customer
                review.save()
                restaurant.avg_rating = Review.objects.calculate_average_rating(restaurant)
                restaurant.save()
                messages.success(request, "Your review has been submitted!")

                return redirect('show_review', restaurant_id=restaurant.id)
        else:
            form = ReviewForm()
        return render(request, 'review/submit_review.html', {'form': form, 'restaurant': restaurant})
    else:
        return redirect('login')
    
@login_required(login_url='login')
def Show_reviews(request,restaurant_id):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        reviews = Review.objects.filter(restaurant=restaurant)
        return render(request,'review/show_review.html',{'restaurant':restaurant, 'reviews':reviews } )

    else:
        return redirect('login')
    
    
    

@login_required(login_url='login')
def like_review(request, review_id):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        review = get_object_or_404(Review, id=review_id)   
        customer = Customer.objects.get(pk=request.user.id)  # Use the primary key of the inherited model
        
        existing_vote = LikeDislike.objects.filter(customer=customer, review=review).first()

        if existing_vote:
            if existing_vote.like:
                messages.info(request, "already liked.")
            else:
                existing_vote.like = True
                existing_vote.save()
                review.likes += 1
                review.dislikes -= 1
                review.save()
                messages.success(request, "like ")
        else:
            LikeDislike.objects.create(customer=customer, review=review, like=True)
            review.likes += 1
            review.save()
            messages.success(request, "like")
        return redirect('show_review', restaurant_id=review.restaurant.id)
    else:
        return redirect('login')

@login_required(login_url='login')
def dislike_review(request, review_id):
    if hasattr(request.user, 'customer') and request.user.customer.is_customer:
        review = get_object_or_404(Review, id=review_id)
        customer = Customer.objects.get(pk=request.user.id)
        
        existing_vote = LikeDislike.objects.filter(customer=customer, review=review).first()

        if existing_vote:
            if not existing_vote.like:
                messages.info(request, "already disliked ")
            else:
                existing_vote.like = False
                existing_vote.save()
                review.likes -= 1
                review.dislikes += 1
                review.save()
                messages.success(request, " dislike.")
        else:
            LikeDislike.objects.create(customer=customer, review=review, like=True)
            review.dislikes += 1
            review.save()
            messages.success(request, "disliked") 
        return redirect('show_review', restaurant_id=review.restaurant.id)
        
    else:
        return redirect('login')
