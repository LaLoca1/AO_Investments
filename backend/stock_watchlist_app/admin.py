from django.contrib import admin
from .models import WatchListItem, WatchListGroup

# Register your models here.

admin.site.register(WatchListItem) 
admin.site.register(WatchListGroup) 