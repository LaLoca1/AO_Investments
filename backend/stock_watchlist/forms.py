# forms.py in your app directory
from django import forms
from .models import WatchListItem, WatchListGroup

class WatchListItemForm(forms.ModelForm):
    class Meta:
        model = WatchListItem
        fields = ['ticker', 'quantity', 'price', 'sector', 'comments', 'group']

class WatchListGroupForm(forms.ModelForm):
    class Meta:
        model = WatchListGroup
        fields = ['name']