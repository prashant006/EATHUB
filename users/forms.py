from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import EatHubAdmin, Customer, RestaurantOwner




class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['user_name', 'name', 'mobile_number', 'email', 'address', 'profile']
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'profile': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


 
class RestaurantOwnerSignUpForm(UserCreationForm):
    class Meta:
        model = RestaurantOwner
        fields = ['user_name', 'name', 'mobile_number', 'email', 'profile']


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile_number']