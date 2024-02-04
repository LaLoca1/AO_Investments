from django.urls import path
from .views import get_stock_news, get_topic_news

urlpatterns = [
    path('api/get_stock_news/<str:ticker>/', get_stock_news, name='get_stock_news'),
    path('api/get_topic_news/<str:topic>/', get_topic_news, name='get_topic_news')
]
