from django.db import models
from datetime import datetime, timedelta
from user_profile.models import UserProfile

# Create your models here.

def default_date(): 
    trade_date = datetime.utcnow() 
    weekday = trade_date.weekday() 
    # 5 - Friday, 6 = Saturday, 0 = Sunday 
    if weekday == 5:
        trade_date -= timedelta(days=1)
    elif weekday == 6: 
        trade_date -= timedelta(days=2) 
    return trade_date 

class WatchListItem(models.Model): 
    ticker = models.CharField(max_length=20, null=False)
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)
    sector = models.CharField(max_length=100, null=False)
    trade_date = models.DateTimeField(default=default_date, verbose_name='Trade Date')
    created_timestamp = models.DateTimeField(default=datetime.utcnow, verbose_name='Created Timestamp')
    comments = models.CharField(max_length=140, null=True, verbose_name='Comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, verbose_name='User')
    group = models.ForeignKey('WatchListGroup', on_delete=models.CASCADE, null=False, verbose_name='Group')

    def __str__(self):
        return f"{self.ticker}"
    
    class Meta:
        verbose_name = 'Watchlist Item' 
        verbose_name_plural = 'Watchlist Items'

class WatchListGroup(models.Model):
    name = models.CharField(max_length=25, null=False, verbose_name='Name')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, verbose_name='User') 
    # watchlist_items = models.ManyToManyField(WatchListItem, verbose_name='Watchlist Items')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Watchlist Group' 
        verbose_name_plural = 'Watchlist Groups'
