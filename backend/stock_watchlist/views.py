# views.py in your app directory
from django.shortcuts import render, redirect
from .models import WatchListItem
from .forms import WatchListItemForm

def watchlist_item_list(request):
    watchlist_items = WatchListItem.objects.all()
    return render(request, 'watchlist_item_list.html', {'watchlist_items': watchlist_items})

def create_watchlist_item(request):
    if request.method == 'POST':
        form = WatchListItemForm(request.POST)
        if form.is_valid():
            watchlist_item = form.save(commit=False)
            watchlist_item.user = request.user.userprofile  # Associate with logged-in user
            watchlist_item.save()
            return redirect('watchlist_item_list')
    else:
        form = WatchListItemForm()

    return render(request, 'create_watchlist_item.html', {'form': form})