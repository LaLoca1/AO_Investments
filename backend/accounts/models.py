from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 

# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None): 
        if not email: 
            raise ValueError("Users must have an email address") 
        
        email = self.normalize_email(email) 
        user = self.model(email=email, username=username)   

        user.set_password(password) 
        user.save() 

        return user 
    
    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password) 

        user.is_superuser = True 
        user.is_staff = True 
        user.save() 

        return user 


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """Database models for the users"""
    email = models.EmailField(max_length=255, unique=True) 
    username = models.CharField(max_length=255) 

    objects = UserAccountManager() 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  

    def get_username(self):
        return self.username 

    def __str__(self):
        return self.email
