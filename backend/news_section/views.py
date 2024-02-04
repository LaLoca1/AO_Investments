from django.http import JsonResponse
import requests
from django.conf import settings
 
def get_stock_news(request, ticker):
    api_key = settings.ALPHA_VANTAGE_API_KEY
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'Error fetching data from Alpha Vantage'}, status=500)