from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
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

class DeleteWatchListItem(APIView):
    permission_classes = [IsAuthenticated] 

    def delete(self, request, pk, format=None):
        # Get the watchlist item or return 404 if not found
        watchlist_item = get_object_or_404(WatchListItems, pk=pk)

        # Ensure the user making the request is the owner of the watchlist item
        if watchlist_item.user == request.user.userprofile:
            watchlist_item.delete()
            return Response({"success": "Watchlist item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You don't have permission to delete the watchlist item"}, status=status.HTTP_403_FORBIDDEN)
        
class EditWatchListItem(APIView):
    permission_classes = [IsAuthenticated] 

    def put(self, request, pk, format=None):
            # Get the watchlist item 
            watchlist_item = get_object_or_404(WatchListItems, pk=pk) 

            # Ensure the user making the request is the owner of the watchlist item
            if watchlist_item.user == request.user.userprofile:
                serializer = WatchListItemSerializer(watchlist_item, data=request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save() 
                    return Response({"detail": "Watchlist item updated successfully"}, status=status.HTTP_200_OK)
                return Response({"detail": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You don't have permission to edit this watchlist item"}, status=status.HTTP_403_FORBIDDEN)



         