# models.py

from django.db import models
from datetime import datetime, timedelta
from user_profile.models import UserProfile

def default_date():
    trade_date = datetime.utcnow()
    weekday = trade_date.weekday()
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
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, verbose_name='User', related_name='watchlist_items')
    group = models.ManyToManyField('WatchListGroup',verbose_name='Group', related_name='watchlist_items')

    def __str__(self):
        return f"{self.ticker}"

    class Meta:
        verbose_name = 'Watchlist Item'
        verbose_name_plural = 'Watchlist Items'

class WatchListGroup(models.Model):
    name = models.CharField(max_length=25, null=False, verbose_name='Name')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, verbose_name='User')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Watchlist Group'
        verbose_name_plural = 'Watchlist Groups'

# Reverse relation from WatchListGroup to WatchListItem
