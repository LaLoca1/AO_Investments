import requests 

from .models import Transaction
from .serializers import TransactionSerializer

from decimal import Decimal
from datetime import datetime, timedelta
from collections import defaultdict, OrderedDict

from django.db.models import Avg, Case, When, Sum, F, IntegerField
from django.db.models.functions import TruncWeek
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

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

# A python class that inherits from APIView            
class SectorBreakdownView(APIView):
    # Sets the permission_classes attribute of SectorBreakdownView to [IsAuthenticated]
    # Means that only authenticated users (users who have valid session) can access this view
    
    permission_classes = [IsAuthenticated] 
    
    # Defines a get method for the class, called when a get request is made to endpoint associated with this view
    # self is used to refer to the instance of a class within class itself. self represents the instance of class SectorbreakdownView
    # allows you to have access to attributes and methods of the class within the method
    # self refers to the view object itself. Its a way for the view to talk about itself and access its own properties and functions
    # Request is a parameter that represents the HTTP request made to the view
    
    def get(self, request):
        # This line retrieves the userprofile associated with the user making the request
        # Assumption here is that there is a one-to-one relationship between Django built in User model 
        # and a custom UserProfile model, and this line detches the user's profile. 
        
        user_profile = request.user.userprofile

        # This is a queryset that represents a query to the database
        # First line queries the database to retrieve transaction data related to user_profile.
        # Filters the transaction model based on the user field matching the user_profile
        # 2nd line further specifies that we want to retrieve values of sector field from filtered transactions.
        # It will group results by sector 
        # 3rd line annotates the queryset by adding a new field 'total_investment'. This calculates total investment in each sector
        # 4th line orders the annotated queryset in descending order based on total_investment field. Means highest total investment 
        # will appear first in the result. 
        sector_data = Transaction.objects.filter(user=user_profile) \
            .values('sector') \
            .annotate(total_investment=Sum(F('price') * F('quantity'))) \
            .order_by('-total_investment')

        # Converts the queryset sector_data into a list and sends it as a response
        # Would look something like this 
        #[ {"sector": "Technology", "total_investment": 50000.0},.....]
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

def get_daily_adjusted_data(ticker, api_key):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "apikey": api_key
    }
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Time Series (Daily)", {})

def get_weekly_adjusted_data(ticker, api_key):
    params = {
        "function": "TIME_SERIES_WEEKLY_ADJUSTED",
        "symbol": ticker,
        "apikey": api_key
    } 
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Weekly Adjusted Time Series", {})

def get_monthly_adjusted_data(ticker, api_key):
    params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": ticker,
        "apikey": api_key
    } 
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Monthly Adjusted Time Series", {})

def get_split_data(ticker, api_key):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "apikey": api_key
    }
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()

    split_data = {}
    if "Time Series (Daily Adjusted)" in data:
        for date, daily_data in data["Time Series (Daily Adjusted)"].items():
            split_coefficient = float(daily_data.get('8. split coefficient', '1.0'))
            if split_coefficient != 1.0:
                split_data[date] = split_coefficient

    return split_data

def get_stock_quantity(user_profile, ticker, date, split_data):
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

    for split_date_str, split_ratio in split_data.items():
        split_date = datetime.strptime(split_date_str, "%Y-%m-%d").date()
        if date >= split_date:
            quantity *= split_ratio

    return max(quantity, 0)

  # Ensure the quantity doesn't go below zero

def get_dividend_data(ticker, api_key):
    params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": ticker,
        "apikey": api_key
    }
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()

    monthly_data = data.get("Monthly Adjusted Time Series", {})
    
    # Store both date and dividend amount
    dividend_info = []
    for date, details in monthly_data.items():
        dividend_amount = float(details.get("7. dividend amount", 0))
        if dividend_amount > 0:
            dividend_info.append({
                "date": date,
                "dividend_amount": dividend_amount
            })

    return dividend_info

class PortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    # takes 2 parameters 'self' which is a ref to instance of the class, and 'ticker' which is the stock 
    # ticker symbol for which you want to fetch the price. 
    def get_current_stock_price(self, ticker):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return float(data["Global Quote"]["05. price"])
        else:
            return None
    
    # a method of a class (as indicated by self parameter). It takes 3 parameters
    def calculate_total_dividends(self, user_profile, ticker, dividend_data): 

        # This line retrieves all transactions from 'Transaction' model for given user and stock ticker, ordered by trade date
        transactions = Transaction.objects.filter(user=user_profile, ticker=ticker).order_by('trade_date')

        # Kepps track of total dividends earned and holding period is an empty list to store the periods which the 
        # user held the stock
        total_dividends = 0 
        holding_periods = [] 

        # Initializes current_hold to none. this variable will later be used to track current holding period of stock
        current_hold = None 
        # The loop processes each transaction. For each 'buy' transaction, it starts a new holding period ('current_hold') and adds it to 
        # 'holding_periods'. For each 'sell' transaction, it ends the current holding period by setting the 'end' date. 
        for transaction in transactions: 
            if transaction.transactionType == 'buy':
                current_hold = {'start': transaction.trade_date.date(), 'end': None} 
                holding_periods.append(current_hold) 
            elif transaction.transactionType == 'sell' and current_hold:
                current_hold['end'] = transaction.trade_date 
                current_hold = None 
        # This checks if theres an ongoing holding period (no sell transactions to end it). If so, it sets the end 
        # date to todays date
        if current_hold and current_hold['end'] is None:
            current_hold['end'] = datetime.today().date() 
        # This loop iterates over each holding period. It assigns the start and end dates of each period, 
        # using today's date if end date is 'None'. 
        for period in holding_periods:
            start_date = period['start']
            end_date = period['end'] if period['end'] is not None else datetime.today().date()
        # This nested loop iterates over each dividend record. It converts the dividend date to a 'date' object 
        # and checks if this date falls within the holding period. If so, adds dividend amount to total_dividends, 
        for dividend in dividend_data:
            dividend_date = datetime.strptime(dividend['date'], "%Y-%m-%d").date()
            if start_date <= dividend_date <= end_date:
                total_dividends += dividend['dividend_amount']

        return total_dividends
    
    def get(self, request):
        user_profile = request.user.userprofile
        # Retrieves the user's portfolio data from the database using a queryset. Aggregates data related to stock transactions 
        # It filters the "Transaction" model to include only transactions associated with the 'user_profile'
        # It groups the data by the 'ticker' field. 
        # It calculates the 'totalQuantity' of stocks based on transaction types (buy and sell) 
        # It calculates the 'averagePrice' of the stocks.
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

        # Prepares the data the be returned as the APi response, iterates over the 'portfolio_items' queryset,and for each item: 
        # Fetches the current stock price using the 'get_current_stock_price' method 
        # Calulates the total investment, current value, and profit or loss for each stock based on the fetched data 
        # It appends the computed data to the 'portfolio_data' list as a dictionary. 
        
        # Initializes empty list which will be used to store dictionaries containing financial metrics for each stock in portfolio
        portfolio_data = []
        # Iterates through each item (each stock) in portfolio_items queryset
        for item in portfolio_items:
            ticker = item['ticker'] 
            split_data = get_split_data(ticker, settings.ALPHA_VANTAGE_API_KEY) 
            dividend_data = get_dividend_data(ticker, settings.ALPHA_VANTAGE_API_KEY)
            total_dividends = self.calculate_total_dividends(user_profile, ticker, dividend_data) 
            adjusted_quantity = get_stock_quantity(user_profile, ticker, datetime.today().date(), split_data)

            current_price = self.get_current_stock_price(item['ticker'])
            if current_price is not None:
                total_investment = adjusted_quantity * item['averagePrice'] + Decimal(total_dividends)
                current_value = adjusted_quantity * current_price 
                profit_or_loss = Decimal(current_value) - total_investment + Decimal(total_dividends) 

                portfolio_data.append({
                    'ticker': item['ticker'],
                    'totalQuantity': item['totalQuantity'],
                    'averagePrice': item['averagePrice'],
                    'totalInvestment': total_investment,
                    'currentValue': current_value,
                    'profitOrLoss': profit_or_loss,
                    'currentPrice': current_price,
                    'totalDividends': total_dividends,
                })
        # This line sends the 'portflio_data' list as a JSON response to the client making the get request
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
    
class PortfolioPerformancePeriodView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile 

        # Group transactions by week and calculate total value
        weekly_data = Transaction.objects.filter(user=user_profile) \
            .annotate(week=TruncWeek('trade_date')) \
            .values('week') \
            .annotate(total_value=Sum(F('price') * F('quantity'))) \
            .order_by('week')

        # Calculate holding period return
        portfolio_performance_data = []
        previous_week_value = None
        for week in weekly_data:
            current_week_value = week['total_value']

            if previous_week_value is not None and previous_week_value != 0:
                # Calculate HPR
                hpr = ((current_week_value - previous_week_value) / previous_week_value) * 100
                portfolio_performance_data.append({
                    'week': week['week'].strftime("%Y-%m-%d"),
                    'holding_period_return': hpr
                })

            previous_week_value = current_week_value

        return Response(portfolio_performance_data)

class DailyPortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user_profile = request.user.userprofile 
        api_key = settings.ALPHA_VANTAGE_API_KEY

        # Define the date range for the last 30 days 
        end_date = datetime.today().date() 
        start_date = end_date - timedelta(days=30) 

        # A queryset taht retrieves a distinct list of stock tickers from the Transaction model for user. Used to fetch historical data for each stock
        tickers = Transaction.objects.filter(user=user_profile).values_list('ticker', flat=True).distinct() 
        # Initializes an ordered dictionary, stores daily performance data. Used to calculate and organize daily portfolio values
        daily_performance = OrderedDict() 

        # Loops over list of tickers and gets daily historical data
        for ticker in tickers:
            historical_data = get_daily_adjusted_data(ticker, api_key) 
            split_data = get_split_data(ticker, api_key)
            # Process data within the last 30 days 
            # extracts daily closing price of stock from historical data 
            # calculates quantity of stock held by user 
            # calculates daily portflio value for that date and stores it in daily_performance
            for date_str, data in historical_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date <= end_date:
                    daily_close_price = float(data['5. adjusted close']) 
                    stock_quantity = get_stock_quantity(user_profile, ticker, date, split_data) 
                    daily_performance[date] = daily_performance.get(date, 0) + stock_quantity * daily_close_price

        formatted_performance = [{
            "day": date.strftime("%Y-%m-%d"),
            "total_value": total_value
        } for date, total_value in daily_performance.items()]

        return Response(formatted_performance)


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
            historical_data = get_weekly_adjusted_data(ticker, api_key)
            split_data = get_split_data(ticker, api_key)
            # Process only data within the last 12 weeks
            for date_str, data in historical_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date <= end_date:
                    weekly_close_price = float(data['5. adjusted close'])
                    stock_quantity = get_stock_quantity(user_profile, ticker, date, split_data)
                    weekly_performance[date] += stock_quantity * weekly_close_price

        # Format and sort the performance data
        formatted_performance = [{"week": date.strftime("%Y-%m-%d"), "total_value": value} for date, value in weekly_performance.items()]
        return Response(sorted(formatted_performance, key=lambda x: x['week']))

class MonthlyPortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        api_key = settings.ALPHA_VANTAGE_API_KEY  # Ideally, this should be in your settings or environment variables
        
        # Define the date range for the last 12 weeks 
        end_date = datetime.today().date() 
        start_date = end_date - timedelta(days=365) 

        # Fetch unique tickers from the user's transactions
        tickers = Transaction.objects.filter(user=user_profile).values_list('ticker', flat=True).distinct()
        # Initialize a structure to hold weekly performance data
        monthly_performance = defaultdict(float)

        for ticker in tickers:
            historical_data = get_monthly_adjusted_data(ticker, api_key)
            split_data = get_split_data(ticker, api_key)
            # Process only data within the last 12 weeks
            for date_str, data in historical_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date <= end_date:
                    monthly_close_price = float(data['5. adjusted close'])
                    stock_quantity = get_stock_quantity(user_profile, ticker, date, split_data)
                    monthly_performance[date] += stock_quantity * monthly_close_price

        # Format and sort the performance data
        formatted_performance = [{"month": date.strftime("%Y-%m"), "total_value": value} for date, value in monthly_performance.items()]
        return Response(sorted(formatted_performance, key=lambda x: x['month']))