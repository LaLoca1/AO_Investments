from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg, Case, When, Sum, F, IntegerField
from django.db.models.functions import TruncWeek
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from .models import Transaction
from .serializers import TransactionSerializer
import requests 
from django.conf import settings
from decimal import Decimal
from datetime import datetime, timedelta
from collections import defaultdict, OrderedDict

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_transaction_items(request):
    user_profile = request.user.userprofile  # Access the userprofile associated with the user
    transaction_items = Transaction.objects.filter(user=user_profile)
    serializer = TransactionSerializer(transaction_items, many=True)
    return Response(serializer.data)
    
class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all() 
    serializer_class = TransactionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile) 

class CreateTransactionView(APIView):
    def post(self, request, *args, **kwargs):
        # Your logic to create a watchlist item here
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.userprofile)  # Associate with logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTransactionView(APIView):
    permission_classes = [IsAuthenticated] 

    def delete(self, request, pk, format=None):
        # Get the watchlist item or return 404 if not found
        transaction_item = get_object_or_404(Transaction, pk=pk)

        # Ensure the user making the request is the owner of the watchlist item
        if transaction_item.user == request.user.userprofile:
            transaction_item.delete()
            return Response({"success": "Transaction deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You don't have permission to delete this transaction"}, status=status.HTTP_403_FORBIDDEN)
        
class EditTransactionView(APIView):
    permission_classes = [IsAuthenticated] 

    def put(self, request, pk, format=None):
            # Get the watchlist item 
            transaction_item = get_object_or_404(Transaction, pk=pk) 

            # Ensure the user making the request is the owner of the watchlist item
            if transaction_item.user == request.user.userprofile:
                serializer = TransactionSerializer(transaction_item, data=request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save() 
                    return Response({"detail": "Transaction updated successfully"}, status=status.HTTP_200_OK)
                return Response({"detail": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You don't have permission to edit this transaction"}, status=status.HTTP_403_FORBIDDEN)

def get_historical_data(ticker, api_key):
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": ticker,
        "apikey": api_key
    }
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Weekly Time Series", {})

def get_daily_historical_data(ticker, api_key):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": api_key
    }
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Time Series (Daily)", {})

def get_stock_quantity(user_profile, ticker, date):
    # Fetch all transactions for the given user and ticker up to the specified date
    transactions = Transaction.objects.filter(
        user=user_profile, 
        ticker=ticker, 
        trade_date__lte=date
    )

    # Initialize quantity
    quantity = 0

    # Sum up the quantities, accounting for buys and sells
    for transaction in transactions:
        if transaction.transactionType == 'buy':
            quantity += transaction.quantity
        elif transaction.transactionType == 'sell':
            quantity -= transaction.quantity

    return max(quantity, 0)  # Ensure the quantity doesn't go below zero


class WeeklyPortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        api_key = settings.ALPHA_VANTAGE_API_KEY  # Ideally, this should be in your settings or environment variables
        
        # Define the date range for the last 12 weeks 
        end_date = datetime.today().date() 
        start_date = end_date - timedelta(weeks=12) 

        # Fetch unique tickers from the user's transactions
        tickers = Transaction.objects.filter(user=user_profile).values_list('ticker', flat=True).distinct()
        # Initialize a structure to hold weekly performance data
        weekly_performance = defaultdict(float)

        for ticker in tickers:
            historical_data = get_historical_data(ticker, api_key)

            # Process only data within the last 12 weeks
            for date_str, data in historical_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date <= end_date:
                    weekly_close_price = float(data['4. close'])
                    stock_quantity = get_stock_quantity(user_profile, ticker, date)
                    weekly_performance[date] += stock_quantity * weekly_close_price

        # Format and sort the performance data
        formatted_performance = [{"week": date.strftime("%Y-%m-%d"), "total_value": value} for date, value in weekly_performance.items()]
        return Response(sorted(formatted_performance, key=lambda x: x['week']))

class DailyPortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user_profile = request.user.userprofile 
        api_key = settings.ALPHA_VANTAGE_API_KEY

        # Define the date range for the last 30 days 
        end_date = datetime.today().date() 
        start_date = end_date - timedelta(days=30) 

        tickers = Transaction.objects.filter(user=user_profile).values_list('ticker', flat=True).distinct() 
        daily_performance = OrderedDict() 

        for ticker in tickers:
            historical_data = get_daily_historical_data(ticker, api_key) 

            # Process data within the last 30 days 
            for date_str, data in historical_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date <= end_date:
                    daily_close_price = float(data['4. close']) 
                    stock_quantity = get_stock_quantity(user_profile, ticker, date) 
                    daily_performance[date] = daily_performance.get(date, 0) + stock_quantity * daily_close_price

        formatted_performance = []
        previous_day_value = None
        for date, total_value in daily_performance.items():
            if previous_day_value is not None and previous_day_value != 0:
                percentage_return = ((total_value - previous_day_value) / previous_day_value) * 100
            else:
                percentage_return = None  # No return for the first day or if previous day's value is zero
            formatted_performance.append({
                "day": date.strftime("%Y-%m-%d"), 
                "total_value": total_value, 
                "percentage_return": percentage_return
            })
            previous_day_value = total_value

        return Response(formatted_performance)
    
class PortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    def get_current_stock_price(self, ticker):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return float(data["Global Quote"]["05. price"])
        else:
            # Handle errors or use a default value/fallback strategy
            return None

    def get(self, request):
        user_profile = request.user.userprofile
        portfolio_items = (
            Transaction.objects.filter(user=user_profile)
            .values('ticker')
            .annotate(
                totalQuantity=Sum(
                    Case(
                        When(transactionType='buy', then='quantity'),
                        When(transactionType='sell', then=-F('quantity')),
                        default=0,
                        output_field=IntegerField()
                    )
                ),
                averagePrice=Avg('price')
            )
            .order_by('ticker')
        )

        portfolio_data = []
        for item in portfolio_items:
            current_price = self.get_current_stock_price(item['ticker'])
            if current_price is not None:
                total_investment = item['totalQuantity'] * item['averagePrice']
                current_value = item['totalQuantity'] * current_price
                profit_or_loss = Decimal(current_value) - total_investment

                portfolio_data.append({
                    'ticker': item['ticker'],
                    'totalQuantity': item['totalQuantity'],
                    'averagePrice': item['averagePrice'],
                    'totalInvestment': total_investment,
                    'currentValue': current_value,
                    'profitOrLoss': profit_or_loss,
                    'currentPrice': current_price
                })

        return Response(portfolio_data)

class PortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user_profile = request.user.userprofile 

        # Group transactions by week 
        weekly_data = Transaction.objects.filter(user=user_profile) \
            .annotate(week=TruncWeek('trade_date')) \
            .values('week') \
            .annotate(total_value=Sum(F('price') * F('quantity'))) \
            .order_by('week')
        
        portfolio_performance_data = [
            {
                'week': week['week'].strftime("%Y-%m-%d"),
                'total_value': week['total_value']
            }
            for week in weekly_data
        ]

        return Response(portfolio_performance_data)
            
class SectorBreakdownView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user_profile = request.user.userprofile

        sector_data = Transaction.objects.filter(user=user_profile) \
            .values('sector') \
            .annotate(total_investment=Sum(F('price') * F('quantity'))) \
            .order_by('-total_investment')

        return Response(list(sector_data))
    
class StockQuantityView(APIView): 
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user_profile = request.user.userprofile 

        stock_data = Transaction.objects.filter(user=user_profile) \
            .values('ticker') \
            .annotate(total_quantity=Sum('quantity')) \
            .order_by('-total_quantity')
        
        return Response(list(stock_data)) 
    
