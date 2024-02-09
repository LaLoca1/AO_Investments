from django.urls import path
from .views import CreateTransactionView, DeleteTransactionView, EditTransactionView, CryptoPortfolioView, CryptoTransactionList, CryptoPortfolioPerformanceView, CryptoPortfolioPerformancePeriodView, DailyCryptoPortfolioPerformanceView, WeeklyCryptoPortfolioPerformanceView, MonthlyCryptoPortfolioPerformanceView 

urlpatterns = [
    path('api/user/crypto-transaction-items/', CryptoTransactionList.as_view(), name='transaction-list'),
    path('api/create-crypto-transaction-item/', CreateTransactionView.as_view(), name='create-transaction'),
    path('api/delete-crypto-transaction-item/<int:pk>/', DeleteTransactionView.as_view(), name='delete-transaction'), 
    path('api/edit-crypto-transaction-item/<int:pk>/', EditTransactionView.as_view(), name='edit-transaction'), 
    path('api/user/crypto-portfolio/', CryptoPortfolioView.as_view(), name='user-crypto-portfolio'), 
    path('api/user/crypto-portfolio-performance/', CryptoPortfolioPerformanceView.as_view(), name='user-crypto-portfolio-performance'), 
    path('api/user/crypto-portfolio-performance-period/', CryptoPortfolioPerformancePeriodView.as_view(), name='user-crypto-portfolio-period-performance'), 
    path('api/user/crypto-daily-portfolio-performance/', DailyCryptoPortfolioPerformanceView.as_view(), name='user-crypto-daily-portfolio-performance'),
    path('api/user/crypto-weekly-portfolio-performance/', WeeklyCryptoPortfolioPerformanceView.as_view(), name='user-crypto-weekly-portfolio-performance'),
    path('api/user/crypto-monthly-portfolio-performance/', MonthlyCryptoPortfolioPerformanceView.as_view(), name='user-crypto-monthly-portfolio-performance'),
]