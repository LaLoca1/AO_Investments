from rest_framework import serializers
from .models import WatchListItem, WatchListGroup

class WatchListGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchListGroup
        fields = '__all__'


class WatchListItemSerializer(serializers.ModelSerializer):
    group = WatchListGroupSerializer(many=True, read_only=True) 

    class Meta: 
        model = WatchListItem
        fields = '__all__' 

        
