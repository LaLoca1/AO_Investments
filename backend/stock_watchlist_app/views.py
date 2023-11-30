from rest_framework import viewsets
from django.shortcuts import render, redirect
from .models import WatchListItem, WatchListGroup
from .forms import WatchListGroupForm, WatchListItemForm
from .serializers import WatchListItemSerializer
from user_profile.models import UserProfile

def create_watchlist_group(request):
    if request.method == 'POST':
        form = WatchListGroupForm(request.POST)
        if form.is_valid():
            watchlist_group = form.save(commit=False)
            
            # Assuming request.user is a User instance
            user_profile = request.user.profile  # Access the UserProfile related to the User
            watchlist_group.user = user_profile
            watchlist_group.save()
            return redirect('create_watchlist_group')
    else:
        form = WatchListGroupForm()

    return render(request, 'stock_watchlist_app/create_watchlist_group.html', {'form': form})

def add_watchlist_item(request):
    if request.method == 'POST':
        form = WatchListItemForm(request.POST)
        if form.is_valid():
            watchlist_item = form.save(commit=False)
            watchlist_item.user = request.user 
            watchlist_item.save()
            return redirect('add_watchlist_item')
    else:
        form = WatchListItemForm() 
    
    return render(request, 'stock_watchlist_app/add_watchlist_item.html', {'form': form}) 
