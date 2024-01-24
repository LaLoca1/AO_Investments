from django.test import TestCase
from django.urls import reverse 
from django.contrib.auth.models import User 
from rest_framework.test import APITestCase, APIClient

# Create your tests here.
class AccountsViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password@123')

    def test_login_success(self):
        url = reverse('login')
        data = {'username' : 'testuser', 'password': 'Password@123'} 
        response = self.client.post(url, data) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'success': 'User authenticated'}) 

    def test_login_failure(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'wrongpassword'} 
        response = self.client.post(url, data) 
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.data) 

    def test_logout(self):
        self.client.login(username='testuser', password='Password@123') 

        url = reverse('logout')
        response = self.client.post(url) 
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data, {'success': 'Logged Out'})

class SignupViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='existinguser', password='Password@123')
    
    def test_signup_success(self):
        url = reverse('signup')
        data = {'username': 'newuser', 'password': 'Password@123', 're_password': 'Password@123'}
        response = self.client.post(url, data) 
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data, { 'success': 'User created successfully' })

    def test_signup_duplicate_username(self):
        # Test signup with an existing username.
        url = reverse('signup')
        data = {'username': 'existinguser', 'password': 'Password@123', 're_password': 'Password@123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'error': 'Username already exists'})

    def test_signup_passwords_do_not_match(self):
        # Test signup with non-matching passwords.
        url = reverse('signup')
        data = {'username': 'user', 'password': 'Password@123', 're_password': 'Password@1234'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'error': 'Passwords do not match'})
    
    def test_signup_short_password(self):
        # Test signup with a short password.
        url = reverse('signup')
        data = {'username': 'user', 'password': '123', 're_password': '123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'error': 'Password must be at least 6 characters'})

class DeleteAccountViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password@123') 
        self.client = APIClient() 
        self.client.login(username='testuser', password='Password@123')

    def test_delete_account_success(self):
        url = reverse('delete')
        response = self.client.delete(url) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, { 'success': 'User deleted successfully' })
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_delete_account_failure(self):
        self.client.logout() 
        url = reverse('delete') 
        response = self.client.delete(url) 
        self.assertNotEqual(response.status_code, 200) 
        self.assertTrue(User.objects.filter(username='testuser').exists()) 
        