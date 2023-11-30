from rest_framework import serializers
from .models import WatchListItem, WatchListGroup

class WatchListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchListItem
        fields = '__all__' 

class WatchListGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchListGroup
        fields = '__all__' 
