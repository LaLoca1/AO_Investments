from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user_profile.models import UserProfile
from stock_watchlist.models import Transaction
from django.urls import reverse 

import datetime 

# Create your tests here.
class CreateTransactionViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password="Password@123")
        self.user_profile = UserProfile.objects.create(user=self.user, first_name='test', last_name='user', email='testuser@gmail.com')
        self.client.login(username='testuser', password='Password@123') 

    def test_create_transaction_success(self):
        url = reverse('create-transaction')
        data = {
            "ticker": "AAPL",
            "quantity": 50,
            "price": 150.00,
            "sector": "Technology",
            "trade_date": "2024-01-01T10:00:00Z",
            "comments": "Purchased after product launch event",
            "transactionType": "buy"
        }
        response = self.client.post(url, data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_transaction_negative_price_failure(self):
        url = reverse('create-transaction')
        data = {
            "ticker": "AAPL",
            "quantity": 50,
            "price": -150.00,
            "sector": "Technology",
            "trade_date": "2024-01-01T10:00:00Z",
            "comments": "Purchased after product launch event",
            "transactionType": "buy"
        }
        response = self.client.post(url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_transaction_negative_quantity_failure(self):
        url = reverse('create-transaction')
        data = {
            "ticker": "AAPL",
            "quantity": -50,
            "price": 150.00,
            "sector": "Technology",
            "trade_date": "2024-01-01T10:00:00Z",
            "comments": "Purchased after product launch event",
            "transactionType": "buy"
        }

    def test_create_transaction_type_failure(self):
        url = reverse('create-transaction')
        data = {
            "ticker": "AAPL",
            "quantity": 50,
            "price": 150.00,
            "sector": "Technology",
            "trade_date": "2024-01-01T10:00:00Z",
            "comments": "Purchased after product launch event",
            "transactionType": "buyy"
        }

        response = self.client.post(url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteTransactionViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password="Password@123")
        self.user_profile = UserProfile.objects.create(user=self.user, first_name='test', last_name='user', email='testuser@gmail.com')
        self.transaction = Transaction.objects.create(
            user=self.user_profile,
            ticker="AAPL",
            quantity=10,
            price=150.00,
            sector="Technology",
            trade_date="2024-01-01T10:00:00Z",
            comments="Test transaction",
            transactionType="buy"
        )
        self.client.login(username='testuser', password='Password@123') 
    
    def test_delete_transaction_success(self):
         url = reverse('delete-transaction', kwargs={'pk': self.transaction.pk}) 
         response = self.client.delete(url) 
         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class EditTransactionViewTest(APITestCase):
     
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password="Password@123")
        self.user_profile = UserProfile.objects.create(user=self.user, first_name='test', last_name='user', email='testuser@gmail.com')
        self.transaction = Transaction.objects.create(
            user=self.user_profile,
            ticker="AAPL",
            quantity=10,
            price=150.00,
            sector="Technology",
            trade_date="2024-01-01T10:00:00Z",
            comments="Test transaction",
            transactionType="buy"
        )

    def test_edit_transaction_success(self): 
        self.client.login(username='testuser', password='Password@123') 
        url = reverse('edit-transaction', kwargs={'pk': self.transaction.pk})
        data = {
                "ticker": "AAPL",
                "quantity": 7,
                "price": 150.00,
                "sector": "Technology",
                "trade_date": "2024-01-01T10:00:00Z",
                "comments": "Stable investment",
                "transactionType": "buy"
            }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_transaction_quantity_failure(self): 
        self.client.login(username='testuser', password='Password@123') 
        url = reverse('edit-transaction', kwargs={'pk': self.transaction.pk})
        data = {
                "ticker": "AAPL",
                "quantity": -7,
                "price": 150.00,
                "sector": "Technology",
                "trade_date": "2024-01-01T10:00:00Z",
                "comments": "Stable investment",
                "transactionType": "buy"
            }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_edit_transaction_quality_failure(self): 
        self.client.login(username='testuser', password='Password@123') 
        url = reverse('edit-transaction', kwargs={'pk': self.transaction.pk})
        data = {
                "ticker": "AAPL",
                "quantity": 7,
                "price": -150.00,
                "sector": "Technology",
                "trade_date": "2024-01-01T10:00:00Z",
                "comments": "Stable investment",
                "transactionType": "buy"
            }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SectorBreakdownViewTest(TestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(username='testuser', password='Password@123')
        self.user_profile = UserProfile.objects.create(user=self.user, first_name='test', last_name='user', email='testuser@gmail.com')

        # Create some transactions
        Transaction.objects.create(
            user=self.user_profile,
            ticker="AAPL",
            quantity=10,
            price=150.00,
            sector="Technology",
            trade_date=datetime.datetime.now(),
            transactionType="buy"
        )
        Transaction.objects.create(
            user=self.user_profile,
            ticker="MSFT",
            quantity=5,
            price=200.00,
            sector="Technology",
            trade_date=datetime.datetime.now(),
            transactionType="buy"
        )

        # Initialize APIClient and authenticate
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_sector_breakdown(self):
        # Make a GET request to the sector breakdown endpoint
        response = self.client.get('/watchlist/api/user/sector-breakdown/')

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        expected_response = [
            {"sector": "Technology", "total_investment": 2500.0}  # Expected data based on the transactions created
        ]
        self.assertEqual(response.json(), expected_response)

class StockQuantityViewTest(TestCase):

    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(username='testuser', password='Password@123')
        self.user_profile = UserProfile.objects.create(user=self.user, first_name='test', last_name='user', email='testuser@gmail.com')

        # Create some test transactions
        Transaction.objects.create(
            user=self.user_profile,
            ticker="AAPL",
            quantity=10,
            price=150.00,
            sector="Technology",
            trade_date=datetime.datetime.now(),
            transactionType="buy"
        )
        Transaction.objects.create(
            user=self.user_profile,
            ticker="MSFT",
            quantity=5,
            price=200.00,
            sector="Technology",
            trade_date=datetime.datetime.now(),
            transactionType="buy"
        )

        # Initialize the APIClient
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_stock_quantity_view(self):
        # Make a GET request to the stock quantity view
        url = reverse("stock-quantity-breakdown")  # Replace with your url name
        response = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(len(response.data), 2)  # Check the number of tickers returned
        self.assertIn({'ticker': 'AAPL', 'total_quantity': 10}, response.data)
        self.assertIn({'ticker': 'MSFT', 'total_quantity': 5}, response.data)
