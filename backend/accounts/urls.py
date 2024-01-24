from django.urls import path 
from .views import SignupView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticatedView,DeleteAccountView,GetUsersView

urlpatterns = [
    path('authenticated', CheckAuthenticatedView.as_view(), name='authenticated'), 
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),  
    path('register', SignupView.as_view(), name='signup'), 
    path('delete', DeleteAccountView.as_view(), name='delete'), 
    path('csrf_cookie', GetCSRFToken.as_view(), name='csrfToken'),  
    path('get_users', GetUsersView.as_view(), name='getUsers'), 
]
