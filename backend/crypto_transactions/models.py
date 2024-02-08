from django.db import models
from user_profile.models import UserProfile
# Create your models here.

class CryptoTransaction(models.Model):

    TRANSACTION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'), 
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    coin = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    trade_date = models.DateTimeField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    comments = models.CharField(max_length=140, blank=True)
    transactionType = models.CharField(max_length=4, choices=TRANSACTION_CHOICES)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.transactionType == 'sell':
                self.apply_fifo() 

        super().save(*args, **kwargs) 

    def apply_fifo(self):
        sell_quantity = self.quantity 

        buy_transactions = CryptoTransaction.objects.filter(
            user=self.user, 
            coin=self.coin, 
            transactionType='buy', 
            quantity__gt = 0 
        ).order_by('trade_date')

        for transaction in buy_transactions:
            if sell_quantity <= 0:
                break 

            if transaction.quantity <= sell_quantity:
                sell_quantity -= transaction.quantity
                transaction.quantity = 0 
            
            else: 
                transaction.quantity -= sell_quantity
                sell_quantity = 0 

            transaction.save(update_fields=['quantity']) 

    
    def __str__(self):
        return f"{self.coin} ({self.transactionType}) - {self.quantity} @ {self.price}"

    class Meta:
        verbose_name = 'Crypto Transaction'
        verbose_name_plural = 'Crypto Transactions'