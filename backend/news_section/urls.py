from django.urls import path
from .views import get_stock_news

urlpatterns = [
    path('api/get_stock_news/<str:ticker>/', get_stock_news, name='get_stock_news'),
]
