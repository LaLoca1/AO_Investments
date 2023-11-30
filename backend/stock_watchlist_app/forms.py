from django import forms 
from .models import WatchListGroup, WatchListItem

class WatchListGroupForm(forms.ModelForm):
    class Meta: 
        model = WatchListGroup
        fields = ['name'] 

class WatchListItemForm(forms.ModelForm):
    class Meta:
        model = WatchListItem
        fields = ['ticker', 'quantity', 'price', 'sector', 'comments', 'group']