from typing import Any
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['food_rating', 'service_rating','delivery_time_rating', 'packaging_rating','order_accuracy_rating', 'review_img', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Write your review here...'}),
            'food_rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rate between 1 and 5'}),
            'service_rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rate between 1 and 5'}),
            'delivery_time_rating': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Rate between 1 and 5'}),
            'packaging_rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rate between 1 and 5'}),
            'order_accuracy_rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rate between 1 and 5'}),
            'review_img': forms.FileInput(attrs={'class': 'form-control'}),
        }
    def clean(self) :
        cleaned_data = super().clean()
        rating_fields = ['food_rating', 'service_rating','delivery_time_rating', 'packaging_rating','order_accuracy_rating']

        for field in rating_fields:
            rating = cleaned_data.get(field)
            if rating is not None:
                if rating < 1 or rating > 5:
                    self.add_error(field, "Rating must be between 1 and 5.")
        
        return cleaned_data
    