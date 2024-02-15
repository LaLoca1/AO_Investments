import requests

from .models import CryptoTransaction
from .serializers import CryptoTransactionSerializer

from decimal import Decimal
from datetime import datetime, timedelta
from collections import defaultdict,OrderedDict

from django.db.models import Avg, Case, When, Sum, F, IntegerField
from django.db.models.functions import TruncWeek
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_transaction_items(request):
    user_profile = request.user.userprofile  # Access the userprofile associated with the user
    transaction_items = CryptoTransaction.objects.filter(user=user_profile)
    serializer = CryptoTransactionSerializer(transaction_items, many=True)
    return Response(serializer.data)
    
class CryptoTransactionList(generics.ListCreateAPIView):
    queryset = CryptoTransaction.objects.all() 
    serializer_class = CryptoTransactionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile) 

class CreateTransactionView(APIView):
    def post(self, request, *args, **kwargs):
        # Your logic to create a watchlist item here
        serializer = CryptoTransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.userprofile)  # Associate with logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTransactionView(APIView):
    permission_classes = [IsAuthenticated] 

    def delete(self, request, pk, format=None):
        # Get the watchlist item or return 404 if not found
        transaction_item = get_object_or_404(CryptoTransaction, pk=pk)

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
            transaction_item = get_object_or_404(CryptoTransaction, pk=pk) 

            # Ensure the user making the request is the owner of the watchlist item
            if transaction_item.user == request.user.userprofile:
                serializer = CryptoTransactionSerializer(transaction_item, data=request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save() 
                    return Response({"detail": "Transaction updated successfully"}, status=status.HTTP_200_OK)
                return Response({"detail": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You don't have permission to edit this transaction"}, status=status.HTTP_403_FORBIDDEN)

def get_crypto_quantity(user_profile, coin, date):
    # Fetch all transactions for the given user and ticker up to the specified date
    transactions = CryptoTransaction.objects.filter(
        user=user_profile, 
        coin=coin, 
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

    return max(quantity, 0)

class CryptoQuantityView(APIView): 
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user_profile = request.user.userprofile 

        crypto_data = CryptoTransaction.objects.filter(user=user_profile) \
            .values('coin') \
            .annotate(total_quantity=Sum('quantity')) \
            .order_by('-total_quantity')
        
        return Response(list(crypto_data)) 
    
def get_daily_crypto_adjusted_data(coin, api_key):
    params = {
        "function": "DIGITAL_CURRENCY_DAILY",
        "symbol": coin,
        "market": "USD",
        "apikey": api_key
    }
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Time Series (Digital Currency Daily)", {})

def get_weekly_crypto_adjusted_data(coin, api_key):
    params = {
        "function": "DIGITAL_CURRENCY_WEEKLY",
        "symbol": coin,
        "apikey": api_key
    } 
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Time Series (Digital Currency Weekly)", {})

def get_monthly_crypto_adjusted_data(coin, api_key):
    params = {
        "function": "DIGITAL_CURRENCY_MONTHLY",
        "symbol": coin,
        "apikey": api_key
    } 
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Time Series (Digital Currency Monthly)", {})

class StockQuantityView(APIView): 
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user_profile = request.user.userprofile 

        crypto_data = CryptoTransaction.objects.filter(user=user_profile) \
            .values('coin') \
            .annotate(total_quantity=Sum('quantity')) \
            .order_by('-total_quantity')
        
        return Response(list(crypto_data)) 

class CryptoPortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    # takes 2 parameters 'self' which is a ref to instance of the class, and 'ticker' which is the stock 
    # ticker symbol for which you want to fetch the price. 
    def get_current_crypto_price(self, coin):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'symbol': coin,
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': settings.COIN_MARKET_CAP_API_KEY
        }

        response = requests.get(url, headers=headers, params=parameters)
        if response.status_code == 200:
            data = response.json()
            price = data['data'][coin]['quote']['USD']['price']
            return float(price)
        else:
            print(f"Error in API request: {response.status_code}")
            return None
                
    def get(self, request):
        user_profile = request.user.userprofile
        crypto_portfolio_items = (
            CryptoTransaction.objects.filter(user=user_profile)
            .values('coin')
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
            .order_by('coin')
        )

        # Prepares the data the be returned as the APi response, iterates over the 'portfolio_items' queryset,and for each item: 
        # Fetches the current stock price using the 'get_current_stock_price' method 
        # Calulates the total investment, current value, and profit or loss for each stock based on the fetched data 
        # It appends the computed data to the 'portfolio_data' list as a dictionary. 
        
        # Initializes empty list which will be used to store dictionaries containing financial metrics for each stock in portfolio
        total_crypto_portfolio_investment = 0 
        total_crypto_portfolio_value = 0 
        total_crypto_portfolio_profit_or_loss = 0 
        
        portfolio_data = []
        # Iterates through each item (each stock) in portfolio_items queryset
        for item in crypto_portfolio_items:
            coin = item['coin'] 
            crypto_quantity = item['totalQuantity']  # Corrected this line

            current_price = self.get_current_crypto_price(coin)
            if current_price is not None:
                total_investment = crypto_quantity * item['averagePrice']
                current_value = crypto_quantity * current_price
                profit_or_loss = Decimal(current_value) - Decimal(total_investment)

                total_crypto_portfolio_investment = total_crypto_portfolio_investment + total_investment
                total_crypto_portfolio_value = total_crypto_portfolio_value + current_value
                total_crypto_portfolio_profit_or_loss = total_crypto_portfolio_profit_or_loss + profit_or_loss

            portfolio_data.append({
                'coin': coin,  # Using the variable 'coin' here for clarity
                'totalQuantity': crypto_quantity,
                'averagePrice': item['averagePrice'],
                'totalInvestment': total_investment,
                'currentValue': current_value,
                'profitOrLoss': profit_or_loss,
                'currentPrice': current_price,
            })
        
        overall_portfolio_data = {
            'totalCryptoPortfolioInvestment': total_crypto_portfolio_investment, 
            'totalCryptoPortfolioValue': total_crypto_portfolio_value,
            'totalCryptoPortfolioProfitOrLoss': total_crypto_portfolio_profit_or_loss
        }

        # This line sends the 'portflio_data' list as a JSON response to the client making the get request
        return Response({
            'CryptoPortfolioData': portfolio_data,
            'overallCryptoPortfolio': overall_portfolio_data})
    
class CryptoPortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user_profile = request.user.userprofile 

        # Group transactions by week 
        weekly_data = CryptoTransaction.objects.filter(user=user_profile) \
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
    
class CryptoPortfolioPerformancePeriodView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile 

        # Group transactions by week and calculate total value
        weekly_data = CryptoTransaction.objects.filter(user=user_profile) \
            .annotate(week=TruncWeek('trade_date')) \
            .values('week') \
            .annotate(total_value=Sum(F('price') * F('quantity'))) \
            .order_by('week')

        # Calculate holding period return
        crypto_portfolio_performance_data = []
        previous_week_value = None
        for week in weekly_data:
            current_week_value = week['total_value']

            if previous_week_value is not None and previous_week_value != 0:
                # Calculate HPR
                hpr = ((current_week_value - previous_week_value) / previous_week_value) * 100
                crypto_portfolio_performance_data.append({
                    'week': week['week'].strftime("%Y-%m-%d"),
                    'holding_period_return': hpr
                })

            previous_week_value = current_week_value

        return Response(crypto_portfolio_performance_data)
    
class DailyCryptoPortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user_profile = request.user.userprofile 
        api_key = settings.ALPHA_VANTAGE_API_KEY

        # Define the date range for the last 30 days 
        end_date = datetime.today().date() 
        start_date = end_date - timedelta(days=30) 

        # A queryset taht retrieves a distinct list of stock tickers from the Transaction model for user. Used to fetch historical data for each stock
        coins = CryptoTransaction.objects.filter(user=user_profile).values_list('coin', flat=True).distinct() 
        # Initializes an ordered dictionary, stores daily performance data. Used to calculate and organize daily portfolio values
        daily_performance = OrderedDict() 

        # Loops over list of tickers and gets daily historical data
        for coin in coins:
            historical_data = get_daily_crypto_adjusted_data(coin, api_key) 
            # Process data within the last 30 days 
            # extracts daily closing price of stock from historical data 
            # calculates quantity of stock held by user 
            # calculates daily portflio value for that date and stores it in daily_performance
            for date_str, data in historical_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date <= end_date:
                    daily_close_price = Decimal(data['4b. close (USD)'])
                    crypto_quantity = get_crypto_quantity(user_profile, coin, date)
                    daily_performance[date] = daily_performance.get(date, Decimal(0)) + crypto_quantity * daily_close_price

        formatted_performance = [{
            "day": date.strftime("%Y-%m-%d"),
            "total_value": total_value
        } for date, total_value in daily_performance.items()]

        return Response(formatted_performance)

class WeeklyCryptoPortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        api_key = settings.ALPHA_VANTAGE_API_KEY  # Ideally, this should be in your settings or environment variables
        
        # Define the date range for the last 12 weeks 
        end_date = datetime.today().date() 
        start_date = end_date - timedelta(weeks=12) 

        # Fetch unique tickers from the user's transactions
        coins = CryptoTransaction.objects.filter(user=user_profile).values_list('coin', flat=True).distinct()
        # Initialize a structure to hold weekly performance data
        weekly_performance = defaultdict(float)

        for coin in coins:
            historical_data = get_weekly_crypto_adjusted_data(coin, api_key)
            # Process only data within the last 12 weeks
            for date_str, data in historical_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date <= end_date:
                    weekly_close_price = Decimal(data['4b. close (USD)'])
                    crypto_quantity = get_crypto_quantity(user_profile, coin, date)
                    weekly_performance[date] = weekly_performance.get(date, Decimal(0)) + crypto_quantity * weekly_close_price

        # Format and sort the performance data
        formatted_performance = [{"week": date.strftime("%Y-%m-%d"), "total_value": value} for date, value in weekly_performance.items()]
        return Response(sorted(formatted_performance, key=lambda x: x['week']))
    
class MonthlyCryptoPortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        api_key = settings.ALPHA_VANTAGE_API_KEY  # Ideally, this should be in your settings or environment variables
        
        # Define the date range for the last 12 weeks 
        end_date = datetime.today().date() 
        start_date = end_date - timedelta(days=365) 

        # Fetch unique tickers from the user's transactions
        coins = CryptoTransaction.objects.filter(user=user_profile).values_list('coin', flat=True).distinct()
        # Initialize a structure to hold weekly performance data
        monthly_performance = defaultdict(float)

        for coin in coins:
            historical_data = get_monthly_crypto_adjusted_data(coin, api_key)
            # Process only data within the last 12 weeks
            for date_str, data in historical_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date <= end_date:
                    monthly_close_price = Decimal(data['4b. close (USD)'])
                    crypto_quantity = get_crypto_quantity(user_profile, coin, date)
                    monthly_performance[date] += monthly_performance.get(date, Decimal(0)) + crypto_quantity * monthly_close_price

        # Format and sort the performance data
        formatted_performance = [{"month": date.strftime("%Y-%m"), "total_value": value} for date, value in monthly_performance.items()]
        return Response(sorted(formatted_performance, key=lambda x: x['month']))