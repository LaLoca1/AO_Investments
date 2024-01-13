from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg, Case, When, Sum, F, IntegerField 
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
            
class PortfolioPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get_stock_time_series_weekly(self, ticker):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={ticker}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            time_series = data.get("Weekly Time Series", {})
            return {date: float(info["4. close"]) for date, info in time_series.items()}
        else:
            return {}

    def get_weekly_portfolio_value(self, user_profile, end_of_week, ticker_prices):
        total_value = Decimal('0.0')
        for ticker, prices in ticker_prices.items():
            if not prices:
                continue  # Skip this ticker if no price data is available

            # Attempt to find the closest date's closing price
            try:
                closest_date = min(prices.keys(), key=lambda d: abs(datetime.strptime(d, '%Y-%m-%d') - end_of_week))
                weekly_price = prices.get(closest_date)
            except ValueError:
                weekly_price = None  # No price data for this week

            if weekly_price:
                # Aggregate the quantity of the ticker up to the end of the week
                quantity = Transaction.objects.filter(
                    user=user_profile,
                    ticker=ticker,
                    trade_date__lte=end_of_week
                ).aggregate(
                    total_quantity=Sum(
                        Case(
                            When(transactionType='buy', then='quantity'),
                            When(transactionType='sell', then=-F('quantity')),
                            default=0,
                            output_field=IntegerField()
                        )
                    )
                )['total_quantity'] or 0

                total_value += Decimal(weekly_price) * Decimal(quantity)

        return total_value

    def get(self, request):
        user_profile = request.user.userprofile
        tickers = Transaction.objects.filter(user=user_profile).values_list('ticker', flat=True).distinct()

        ticker_prices = {ticker: self.get_stock_time_series_weekly(ticker) for ticker in tickers}

        end_date = datetime.today()
        start_date = end_date - timedelta(days=90) # Rolling period of 90 days

        # Generate a list of end-of-week dates between start_date and end_date
        weeks = [start_date + timedelta(days=(6 - start_date.weekday()) + i * 7) for i in range((end_date - start_date).days // 7 + 1)]

        portfolio_values = []
        for end_of_week in weeks:
            weekly_value = self.get_weekly_portfolio_value(user_profile, end_of_week, ticker_prices)
            portfolio_values.append({
                'week': end_of_week.strftime('%Y-%m-%d'),
                'totalValue': weekly_value
            })

        return Response(portfolio_values)
    
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
         