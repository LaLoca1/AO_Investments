# views.py in your app directory
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics 
from .models import WatchListItem, WatchListGroup
from .serializers import WatchListItemSerializer, WatchListGroupSerializer
from .forms import WatchListItemForm, WatchListGroupForm

class WatchListItemList(generics.ListCreateAPIView):
    queryset = WatchListItem.objects.all() 
    serializer_class = WatchListItemSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile) 

class WatchlistItemCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Your logic to create a watchlist item here
        serializer = WatchListItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.userprofile)  # Associate with logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchListGroupList(generics.ListCreateAPIView):
    queryset = WatchListGroup.objects.all() 
    serializer_class = WatchListGroupSerializer

def watchlist_item_list(request):
    watchlist_items = WatchListItem.objects.all()
    return render(request, 'watchlist_item_list.html', {'watchlist_items': watchlist_items})

def create_watchlist_item(request):
    if request.method == 'POST':
        form = WatchListItemForm(request.POST)
        if form.is_valid():
            watchlist_item = form.save(commit=False)
            watchlist_item.user = request.user.userprofile  # Associate with logged-in user
            watchlist_item.save()
            return redirect('watchlist_item_list')
    else:
        form = WatchListItemForm()

    return render(request, 'create_watchlist_item.html', {'form': form})


def create_watchlist(request):
    if request.method == 'POST':
        form = WatchListGroupForm(request.POST)
        if form.is_valid():
            watchlist = form.save(commit=False)
            watchlist.user = request.user.userprofile  # Associate with logged-in user
            watchlist.save()
            return redirect('watchlist_detail', watchlist_name=watchlist.name)
    else:
        form = WatchListGroupForm()

    return render(request, 'create_watchlist.html', {'form': form})

def watchlist_detail(request, watchlist_name):
    watchlist = get_object_or_404(WatchListGroup, name=watchlist_name, user=request.user.userprofile)
    watchlist_items = watchlist.watchlist_items.all()
    return render(request, 'watchlist_detail.html', {'watchlist': watchlist, 'watchlist_items': watchlist_items})