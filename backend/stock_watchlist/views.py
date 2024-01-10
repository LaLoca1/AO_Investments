from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import PermissionDenied
from rest_framework import status, generics, permissions
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_transaction_items(request):
    user_profile = request.user.userprofile  # Access the userprofile associated with the user
    transaction_items = Transaction.objects.filter(user=user_profile)
    serializer = TransactionSerializer(transaction_items, many=True)
    return Response(serializer.data)
    
class TransactionList(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        """
        This view should return a list of all transactions for the currently authenticated user.
        """
        user_profile = self.request.user.userprofile
        return Transaction.objects.filter(user=user_profile) 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile) 

class CreateTransactionView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile) 

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all() 
    serializer_class = TransactionSerializer
    permissions_classes = [permissions.IsAuthenticated] 

    def get_object(self):
        transaction = super().get_object() 
        if transaction.user != self.request.user.userprofile: 
            raise PermissionDenied("You do not have permission to access this transaction")
        return transaction
    
    def perform_update(self, serializer):
        serializer.save() 
         