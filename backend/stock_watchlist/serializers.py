from rest_framework import serializers
from .models import WatchListItems, WatchListGroup

class WatchListGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchListGroup
        fields = '__all__'
        read_only_fields = ['user']

class WatchListItemSerializer(serializers.ModelSerializer):
    group = WatchListGroupSerializer(read_only=True)

    class Meta: 
        model = WatchListItems
        fields = '__all__' 
        read_only_fields = ['user']
