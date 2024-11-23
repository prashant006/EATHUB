from.models import Restaurant, RestaurantMenu
from django import forms


class AddRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [ 'name', 'email', 'location', 'cuisine_type', 'open_at', 'close_at', 'contact_info','restaurant_img']

    open_at = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    close_at = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))


class AddDishForm(forms.ModelForm):
    class Meta:
        model = RestaurantMenu
        fields = ['dish_name', 'discription', 'dish_image', 'price']
    