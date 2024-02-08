from django.urls import path
from .views import CreateTransactionView, DeleteTransactionView, EditTransactionView, CryptoPortfolioView, CryptoTransactionList
urlpatterns = [
    path('api/user/crypto-transaction-items/', CryptoTransactionList.as_view(), name='transaction-list'),
    path('api/create-crypto-transaction-item/', CreateTransactionView.as_view(), name='create-transaction'),
    path('api/delete-crypto-transaction-item/<int:pk>/', DeleteTransactionView.as_view(), name='delete-transaction'), 
    path('api/edit-crypto-transaction-item/<int:pk>/', EditTransactionView.as_view(), name='edit-transaction'), 
    path('api/user/crypto-portfolio/', CryptoPortfolioView.as_view(), name='user-crypto-portfolio'), 
]