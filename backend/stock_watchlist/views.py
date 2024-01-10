from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from .models import Transaction
from .serializers import TransactionSerializer, PortfolioSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_transaction_items(request):
    user_profile = request.user.userprofile  # Access the userprofile associated with the user
    transaction_items = Transaction.objects.filter(user=user_profile)
    serializer = TransactionSerializer(transaction_items, many=True)
    return Response(serializer.data)
    
class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all() 
    serializer_class = TransactionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile) 

class CreateTransactionView(APIView):
    def post(self, request, *args, **kwargs):
        # Your logic to create a watchlist item here
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.userprofile)  # Associate with logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTransactionView(APIView):
    permission_classes = [IsAuthenticated] 

    def delete(self, request, pk, format=None):
        # Get the watchlist item or return 404 if not found
        transaction_item = get_object_or_404(Transaction, pk=pk)

        # Ensure the user making the request is the owner of the watchlist item
        if transaction_item.user == request.user.userprofile:
            transaction_item.delete()
            return Response({"success": "Transaction deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You don't have permission to delete this transaction"}, status=status.HTTP_403_FORBIDDEN)
        
class EditTransactionView(APIView):
    permission_classes = [IsAuthenticated] 

    def put(self, request, pk, format=None):
            # Get the watchlist item 
            transaction_item = get_object_or_404(Transaction, pk=pk) 

            # Ensure the user making the request is the owner of the watchlist item
            if transaction_item.user == request.user.userprofile:
                serializer = TransactionSerializer(transaction_item, data=request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save() 
                    return Response({"detail": "Transaction updated successfully"}, status=status.HTTP_200_OK)
                return Response({"detail": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You don't have permission to edit this transaction"}, status=status.HTTP_403_FORBIDDEN)

class PortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile 
        portfolio_items = (
            Transaction.objects.filter(user=user_profile)
            .values('ticker')
            .annotate(totalQuantity=Sum('quantity'), averagePrice=Avg('price')) 
            .order_by('ticker')
        )
        serializer = PortfolioSerializer(portfolio_items, many=True) 
        return Response(serializer.data) 

         