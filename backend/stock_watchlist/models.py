from django.db import models
from datetime import timedelta
from user_profile.models import UserProfile
from django.utils import timezone 
import pytz 

UK_PUBLIC_HOLIDAYS = [
    '2023-01-01', '2023-04-07', '2023-04-10', # New Year's Day, Good Friday, Easter Monday
    '2023-05-01', '2023-05-29', '2023-08-28', # Early May Bank Holiday, Spring Bank Holiday, Summer Bank Holiday
    '2023-12-25', '2023-12-26', # Christmas Day, Boxing Day
]

US_PUBLIC_HOLIDAYS = [
    '2023-01-01', '2023-07-04', '2023-11-11',  # New Year's Day, Independence Day, Veterans Day
    '2023-11-23', '2023-12-25',                # Thanksgiving Day, Christmas Day
    # Add more holidays as needed
]

def default_trade_date(market):
    if market == 'UK':
        holidays_list = UK_PUBLIC_HOLIDAYS
        timezone_name = 'Europe/London'
    elif market == 'US':
        holidays_list = US_PUBLIC_HOLIDAYS
        timezone_name = 'America/New_York'
    else:
        raise ValueError("Invalid market")

    trade_date = timezone.now().astimezone(pytz.timezone(timezone_name)).date()

    while trade_date.weekday() >= 5 or trade_date.isoformat() in holidays_list:
        trade_date -= timedelta(days=1)

    return trade_date

class Transaction(models.Model):
    MARKET_CHOICES = [
        ('UK', 'United Kingdom'),
        ('US', 'United States'), 
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sector = models.CharField(max_length=100)
    market = models.CharField(max_length=2, choices=MARKET_CHOICES, default='US')
    trade_date = models.DateTimeField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    comments = models.CharField(max_length=140, blank=True)
    transactionType = models.CharField(max_length=4, choices=[
        ('buy', 'Buy'), 
        ('sell', 'Sell'),
    ])

    def save(self, *args, **kwargs):
        if not self.pk: # Checking if it's a new instance
            self.trade_date = default_trade_date(self.market) 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.ticker} ({self.transactionType}) - {self.quantity} @ {self.price}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
