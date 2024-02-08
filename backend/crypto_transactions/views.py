import requests

from .models import CryptoTransaction
from .serializers import CryptoTransactionSerializer

from decimal import Decimal
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.db.models import Avg, Case, When, Sum, F, IntegerField
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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
        "function": "TIME_SERIES_WEEKLY_ADJUSTED",
        "symbol": coin,
        "apikey": api_key
    } 
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Weekly Adjusted Time Series", {})

def get_monthly_crypto_adjusted_data(coin, api_key):
    params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": coin,
        "apikey": api_key
    } 
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    return data.get("Monthly Adjusted Time Series", {})

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
        portfolio_items = (
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
        portfolio_data = []
        # Iterates through each item (each stock) in portfolio_items queryset
        for item in portfolio_items:
            coin = item['coin'] 
            crypto_quantity = item['totalQuantity']  # Corrected this line

            current_price = self.get_current_crypto_price(coin)
            if current_price is not None:
                total_investment = crypto_quantity * item['averagePrice']
                current_value = crypto_quantity * current_price
                profit_or_loss = Decimal(current_value) - Decimal(total_investment)

            portfolio_data.append({
                'coin': coin,  # Using the variable 'coin' here for clarity
                'totalQuantity': crypto_quantity,
                'averagePrice': item['averagePrice'],
                'totalInvestment': total_investment,
                'currentValue': current_value,
                'profitOrLoss': profit_or_loss,
                'currentPrice': current_price,
            })
        # This line sends the 'portflio_data' list as a JSON response to the client making the get request
        return Response(portfolio_data)