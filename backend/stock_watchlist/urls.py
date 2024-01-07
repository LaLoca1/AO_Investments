from django.urls import path
from .views import WatchListItemList, WatchListItemCreateView, DeleteWatchListItem, EditWatchListItem, get_stock_data, user_watchlist_items

urlpatterns = [
    path('api/watchlist-items', WatchListItemList.as_view(), name='watchlist-item-list'),
    path('api/create-watchlist-item', WatchListItemCreateView.as_view(), name='watchlist-item-create'),
    path('api/delete-watchlist-item/<int:pk>', DeleteWatchListItem.as_view(), name='delete-watchlist-item'), 
    path('api/edit-watchlist-item/<int:pk>', EditWatchListItem.as_view(), name='edit-watchlist-item'), 
    path('api/user/watchlist-items', user_watchlist_items, name='user-watchlist-items'),
    path('api/stock/<str:ticker>/', get_stock_data, name='get_stock_data'), 
]
