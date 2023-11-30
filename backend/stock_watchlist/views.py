# views.py in your app directory
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import WatchListItem, WatchListGroup
from .forms import WatchListItemForm, WatchListGroupForm

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


def create_watchlist(request):
    if request.method == 'POST':
        form = WatchListGroupForm(request.POST)
        if form.is_valid():
            watchlist = form.save(commit=False)
            watchlist.user = request.user.userprofile  # Associate with logged-in user
            watchlist.save()
            return redirect('watchlist_detail', watchlist_name=watchlist.name)
    else:
        form = WatchListGroupForm()

    return render(request, 'create_watchlist.html', {'form': form})

def watchlist_detail(request, watchlist_name):
    watchlist = get_object_or_404(WatchListGroup, name=watchlist_name, user=request.user.userprofile)
    watchlist_items = watchlist.watchlist_items.all()
    return render(request, 'watchlist_detail.html', {'watchlist': watchlist, 'watchlist_items': watchlist_items})