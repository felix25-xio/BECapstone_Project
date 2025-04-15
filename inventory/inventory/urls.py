from django.urls import path, include
from .views import (
    CategoryListCreateView, 
    CategoryDetailView, 
    InventoryItemListCreateView, 
    InventoryItemDetailView
)
from rest_framework.routers import DefaultRouter
from .views import (
    InventoryChangeViewSet, 
    UserViewSet, 
    InventoryLevelView, 
    InventoryChangeHistoryView, 
    RegisterView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Routers
router = DefaultRouter()
router.register(r'inventory-changes', InventoryChangeViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('inventory/', InventoryItemListCreateView.as_view(), name='inventory-list-create'),
    path('inventory/<int:pk>/', InventoryItemDetailView.as_view(), name='inventory-detail'),
    path('', include(router.urls)),
    path('inventory-levels/', InventoryLevelView.as_view(), name='inventory-levels'),
    path('inventory/<int:item_id>/changes/', InventoryChangeHistoryView.as_view(), name='inventory-change-history'),
]