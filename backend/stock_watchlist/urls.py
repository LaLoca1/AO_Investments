# urls.py in your app directory
from django.urls import path
from .views import watchlist_item_list, create_watchlist_item, create_watchlist, watchlist_detail

urlpatterns = [
    path('watchlist_items', watchlist_item_list, name='watchlist_item_list'),
    path('create_watchlist_item', create_watchlist_item, name='create_watchlist_item'),
    path('create_watchlist', create_watchlist, name='create_watchlist'),
    path('watchlistgroup/<str:watchlist_name>', watchlist_detail, name='watchlist_detail'),
    # Add more URLs as needed
]
