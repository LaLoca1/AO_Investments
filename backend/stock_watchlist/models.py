from django.db import models
from datetime import datetime, timedelta
from user_profile.models import UserProfile

def default_date():
    trade_date = datetime.utcnow()
    weekday = trade_date.weekday()
    if weekday == 6:
        trade_date -= timedelta(days=1)
    elif weekday == 7:
        trade_date -= timedelta(days=2)
    return trade_date

class WatchListGroup(models.Model):
    name = models.CharField(max_length=25, null=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Watchlist Group'
        verbose_name_plural = 'Watchlist Groups'

class WatchListItems(models.Model):
    ticker = models.CharField(max_length=20, null=False)
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)
    sector = models.CharField(max_length=100, null=False)
    trade_date = models.DateTimeField(default=default_date)
    created_timestamp = models.DateTimeField(default=datetime.utcnow)
    comments = models.CharField(max_length=140, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False)
    group = models.ForeignKey(WatchListGroup, on_delete=models.CASCADE, related_name='watchlist_items')

    def __str__(self):
        return f"{self.ticker}"

    class Meta:
        verbose_name = 'Watchlist Item'
        verbose_name_plural = 'Watchlist Items'

