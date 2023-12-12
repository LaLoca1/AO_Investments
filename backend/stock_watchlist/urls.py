from django.urls import path
from .views import WatchListItemList, WatchListItemCreateView, user_watchlist_items

urlpatterns = [
    path('api/watchlist-items', WatchListItemList.as_view(), name='watchlist-item-list'),
    path('api/create-watchlist-item', WatchListItemCreateView.as_view(), name='watchlist-item-create'),
    path('api/user/watchlist-items', user_watchlist_items, name='user-watchlist-items'),
]
