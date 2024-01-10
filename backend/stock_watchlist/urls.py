from django.urls import path
from .views import TransactionList, PortfolioView, CreateTransactionView, DeleteTransactionView, EditTransactionView, user_transaction_items

urlpatterns = [
    path('api/transaction-items/', TransactionList.as_view(), name='transaction-list'),
    path('api/create-transaction-item/', CreateTransactionView.as_view(), name='create-transaction'),
    path('api/delete-transaction-item/<int:pk>/', DeleteTransactionView.as_view(), name='delete-transaction'), 
    path('api/edit-transaction-item/<int:pk>/', EditTransactionView.as_view(), name='edit-transaction'), 
    path('api/user/portfolio/', PortfolioView.as_view(), name='user-portfolio'), 
    path('api/user/transaction-items/', user_transaction_items, name='user-transaction-items'),
]
