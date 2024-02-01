from django.db import models
from datetime import timedelta, datetime # Used to work with time duration
from user_profile.models import UserProfile # Custom model for user profiles


def default_trade_date():

    now = datetime.now() 

    trade_date = now.date() 

    if trade_date.weekday() == 5:
        trade_date -= timedelta(days=1) 
    elif trade_date.weekday() == 6:
        trade_date -= timedelta(days=2) 
    
    return trade_date

class Transaction(models.Model):

    TRANSACTION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'), 
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sector = models.CharField(max_length=100)
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
