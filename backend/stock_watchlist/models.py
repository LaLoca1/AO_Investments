from django.db import models
from datetime import timedelta # Used to work with time duration
from user_profile.models import UserProfile # Custom model for user profiles
from django.utils import timezone # To work with timezones
import pytz # work with timezones and handle holidays

# This defines a list of public holidays in US and UK markets
UK_PUBLIC_HOLIDAYS = [
    '2023-01-01', '2023-04-07', '2023-04-10', # New Year's Day, Good Friday, Easter Monday
    '2023-05-01', '2023-05-29', '2023-08-28', # Early May Bank Holiday, Spring Bank Holiday, Summer Bank Holiday
    '2023-12-25', '2023-12-26', # Christmas Day, Boxing Day
]

US_PUBLIC_HOLIDAYS = [
    '2023-01-01', '2023-07-04', '2023-11-11',  # New Year's Day, Independence Day, Veterans Day
    '2023-11-23', '2023-12-25',                # Thanksgiving Day, Christmas Day
]

# Takes a market parameter 
def default_trade_date(market):
    # Get the current date and time with timezone information
    now = timezone.now()

    # Adjust the timezone based on the market
    if market == 'UK':
        tz = pytz.timezone('Europe/London')
        holidays_list = UK_PUBLIC_HOLIDAYS
    elif market == 'US':
        tz = pytz.timezone('America/New_York')
        holidays_list = US_PUBLIC_HOLIDAYS
    else:
        raise ValueError("Invalid market")

    # Convert 'now' to the market's timezone
    trade_datetime = now.astimezone(tz)

    # Extract just the date part
    trade_date = trade_datetime.date()

    # Adjust for weekends and market-specific holidays
    # This enters a loop to adjust the trade_date, if it falls on weekend or matches any holiday 
    # It keeps subtracting one day at a time until it finds a valid trade date. 
    while trade_date.weekday() >= 5 or trade_date.isoformat() in holidays_list:
        trade_date -= timedelta(days=1)

    # Replaces the year, month & day of trade_datetime with adjusted trade_date values & returns 
    # the resulting datetime. This adjusted datetime represents the default trade date for the 
    # specified market, considering weekends and holidays 
    return trade_datetime.replace(year=trade_date.year, month=trade_date.month, day=trade_date.day)

class Transaction(models.Model):
    MARKET_CHOICES = [
        ('UK', 'United Kingdom'),
        ('US', 'United States'), 
    ]
    TRANSACTION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'), 
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
    transactionType = models.CharField(max_length=4, choices=TRANSACTION_CHOICES)
    
    # this is a 'save' method of a django model class, it is called automatically when an instance of the model is saved in database
    def save(self, *args, **kwargs):
        if not self.pk: # Checking if it's a new instance
            if self.transactionType == 'sell':
                self.apply_fifo() 
                # This ensures that the quantity sold is deducted from earliest bought stocks (based on trade date) first

        super().save(*args, **kwargs)
        # After performing necessary actions for new instances, calls the 'save' method of parent class using super()
        # Ensures that the instance is saved to the database as usual. 

    # method of the model class, responsible for applying the fifo logic when selling stocks
    def apply_fifo(self):
        # Initializes the sell quantity with the total quantity to be sold from current instance
        sell_quantity = self.quantity 
        # queries database to retrieve all prev 'buy' transactions for same user, ticker... 
        # where the quantity is greater than 0 (indicating availible stocks to sell). Result ordered by trade date 
        buy_transactions = Transaction.objects.filter(
            user=self.user, 
            ticker=self.ticker, 
            transactionType='buy', 
            quantity__gt = 0 
        ).order_by('trade_date')

        for transaction in buy_transactions:
            if sell_quantity <= 0: # Checks if there are still stocks to be sold, if not breaks out of loop
                break 
            
            # check if quantity of current 'buy' transaction is less than or equal to sell_quantity. If it is the case 
            # means that the entire quantity of this 'buy' transaction can be used to fulfill sell order. So it subtracts this quantity
            # from 'sell_quantity' and sets transaction.quantity to 0, indicating these stocks have been fully sold
            if transaction.quantity <= sell_quantity:
                sell_quantity -= transaction.quantity
                transaction.quantity = 0 
            
            else: 
                transaction.quantity -= sell_quantity
                sell_quantity = 0 

            transaction.save(update_fields=['quantity']) 

    
    def __str__(self):
        return f"{self.ticker} ({self.transactionType}) - {self.quantity} @ {self.price}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
