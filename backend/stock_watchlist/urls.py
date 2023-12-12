from django.urls import path
from .views import WatchListItemList, WatchListGroupList, WatchListItemCreateView, WatchListGroupCreateView

urlpatterns = [
    path('api/watchlist-items', WatchListItemList.as_view(), name='watchlist-item-list'),
    path('api/create-watchlist-item', WatchListItemCreateView.as_view(), name='watchlist-item-create'),
    path('api/watchlist-groups', WatchListGroupList.as_view(), name='watchlist-group-list'),
    path('api/create-watchlist-group', WatchListGroupCreateView.as_view(), name='create-watchlist-group-list'),
]
