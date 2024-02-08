from rest_framework import serializers
from .models import CryptoTransaction

class CryptoTransactionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CryptoTransaction
        fields = '__all__' 
        read_only_fields = ['user']
        
    def validate_price(self, value):
        """
        Check that the price is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return value
    
class CryptoPortfolioSerializer(serializers.Serializer):
    ticker = serializers.CharField() 
    totalQuantity = serializers.IntegerField()
    averagePrice = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False) 