from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from .models import WatchListItems
from .serializers import WatchListItemSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_watchlist_items(request):
    user_profile = request.user.userprofile  # Access the userprofile associated with the user
    watchlist_items = WatchListItems.objects.filter(user=user_profile)
    serializer = WatchListItemSerializer(watchlist_items, many=True)
    return Response(serializer.data)
    
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
