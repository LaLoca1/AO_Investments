from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import WatchListItems, WatchListGroup
from .serializers import WatchListItemSerializer, WatchListGroupSerializer

# Create your views here.
class WatchListItemList(generics.ListCreateAPIView):
    queryset = WatchListItems.objects.all() 
    serializer_class = WatchListItemSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile) 

class WatchListItemCreateView(APIView):
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

class WatchListGroupCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Your logic to create a watchlist item here
        serializer = WatchListGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.userprofile)  # Associate with logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)