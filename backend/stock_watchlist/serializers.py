from rest_framework import serializers
from .models import WatchListItems

class WatchListItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = WatchListItems
        fields = '__all__' 
        read_only_fields = ['user']
