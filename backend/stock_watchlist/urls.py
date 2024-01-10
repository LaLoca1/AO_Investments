from django.urls import path
from .views import TransactionList, CreateTransactionView, TransactionDetail, user_transaction_items

urlpatterns = [
    path('api/transaction-items/', TransactionList.as_view(), name='transaction-list'),
    path('api/create-transaction-item/', CreateTransactionView.as_view(), name='create-transaction'),
    path('api/transaction-item/<int:pk>/', TransactionDetail.as_view(), name='transaction-detail'),  # Consolidated view
    path('api/user/transaction-items/', user_transaction_items, name='user-transaction-items'),
]
