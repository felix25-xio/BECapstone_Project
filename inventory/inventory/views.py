from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import RegisterSerializer
from rest_framework import generics, viewsets, permissions, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InventoryItem, Category, InventoryChange
from .serializers import InventoryItemSerializer, CategorySerializer, InventoryChangeSerializer, UserSerializer

# Create your views here.

# Registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer



# Category API
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# InventoryItem API
class InventoryItemListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only logged-in users can modify
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'quantity', 'price', 'date_added']  # Fields users can sort by
    ordering = ['name']  # Default sort order

    def perform_create(self, serializer):
        serializer.save(managed_by=self.request.user)  # Assign item to logged-in user

class InventoryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def perform_destroy(self, serializer):
        serializer.delete()


    def perform_update(self, serializer):
        # Get the existing item before update
        original_item = self.get_object()
        old_quantity = original_item.quantity
        updated_original_item = serializer.save()

        new_quantity = updated_original_item.quantity

        if old_quantity != new_quantity:
            quantity_changed = abs(new_quantity - old_quantity)
            change_type = 'restock' if new_quantity > old_quantity else 'sale'

            InventoryChange.objects.create(
                item=updated_original_item,
                changed_by=self.request.user,
                change_type=change_type,
                quantity_changed=quantity_changed
            )

        # Save updated item
        updated_item = serializer.save()

        # Log if quantity has changed
        if updated_item.quantity != old_quantity:
            InventoryChange.objects.create(
                item=updated_item,
                change_type='update',
                quantity_changed=updated_item.quantity - old_quantity,
                changed_by=self.request.user
            )


class InventoryChangeViewSet(viewsets.ModelViewSet):
    queryset = InventoryChange.objects.all()
    serializer_class = InventoryChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(changed_by=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InventoryLevelView(APIView):
    def get(self, request):
        queryset = InventoryItem.objects.all()

        # Filter by category
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        # Filter by price range
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Filter by low stock (e.g., quantity less than threshold)
        low_stock = request.GET.get('low_stock')
        if low_stock:
            try:
                threshold = int(low_stock)
                queryset = queryset.filter(quantity__lt=threshold)
            except ValueError:
                return Response({"error": "Invalid low_stock threshold"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize results
        serializer = InventoryItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# View to show Inventory Change History
class InventoryChangeHistoryView(generics.ListAPIView):
    serializer_class = InventoryChangeSerializer

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return InventoryChange.objects.filter(item_id=item_id).order_by('-change_date')