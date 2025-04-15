from django.contrib.auth.models import User
from rest_framework import serializers
from .models import InventoryItem, Category, InventoryChange


# Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class InventoryItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Show category details
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = InventoryItem
        fields = ['id', 'sku', 'name', 'description', 'quantity', 'price', 'category', 'category_id', 'date_added', 'last_updated', 'managed_by']


# serializers for inventory update
class InventoryChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryChange
        fields = '__all__'
        read_only_fields = ['changed_by', 'change_date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user