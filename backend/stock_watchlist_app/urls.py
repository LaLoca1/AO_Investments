# urls.py
from django.urls import path
from .views import create_watchlist_group, add_watchlist_item

urlpatterns = [
    path('create_watchlist_group', create_watchlist_group, name='create_watchlist_group'),
    path('add_watchlist_item', add_watchlist_item, name='add_watchlist_item'),
    # Add other URL patterns as needed
]
