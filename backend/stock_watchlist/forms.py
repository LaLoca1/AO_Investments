# forms.py in your app directory
from django import forms
from .models import WatchListItem

class WatchListItemForm(forms.ModelForm):
    class Meta:
        model = WatchListItem
        fields = ['ticker', 'quantity', 'price', 'sector', 'comments', 'group']
