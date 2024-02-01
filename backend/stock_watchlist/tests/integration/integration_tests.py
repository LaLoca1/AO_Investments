from django.test import TestCase
from django.urls import reverse 
from rest_framework import status 
from stock_watchlist.models import Transaction 
from user_profile.models import UserProfile
from django.contrib.auth.models import User 
from rest_framework.test import APIClient

class UserTransactionIntegrationTest(TestCase):
    """This tests a sequence of actions in an integration test designed to test a sequence 
    of actions involving user signup, login, transaction creation, and logout"""
    
    def setUp(self):
        self.client = APIClient() 

        self.signup_url = reverse('signup')
        self.login_url = reverse('login') 
        self.create_transaction_url = reverse('create-transaction') 
        self.logout_url = reverse('logout') 

        self.user_data = {
            'username': 'testuser',
            'password': 'Password@123',
            're_password': 'Password@123',
        }

        self.transaction_data = {
            "ticker": "AAPL",
            "quantity": 50,
            "price": 150.00,
            "sector": "Technology",
            "trade_date": "2024-01-01T10:00:00Z",
            "comments": "Purchased after product launch event",
            "transactionType": "buy"
        }

    def test_user_signup_login_transaction_logout(self):

        response = self.client.post(self.signup_url, self.user_data) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.create_transaction_url, self.transaction_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='testuser')
        user_profile = UserProfile.objects.get(user=user) 
        transaction = Transaction.objects.filter(user=user_profile, ticker='AAPL').first() 
        self.assertIsNotNone(transaction) 

        response = self.client.post(self.logout_url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)


