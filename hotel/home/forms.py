from django import forms
from .models import Hotel

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('hotel_name', 'hotel_price','description','amenities', 'people_capacity')
