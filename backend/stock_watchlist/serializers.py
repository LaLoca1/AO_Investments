from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Transaction
        fields = '__all__' 
        read_only_fields = ['user']

class PortfolioSerializer(serializers.Serializer):
    ticker = serializers.CharField() 
    totalQuantity = serializers.IntegerField()
    averagePrice = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False) 