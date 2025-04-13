from django.contrib import admin
from .models import Category, InventoryItem, InventoryChange

# Register your models here.

class InventoryChangeInline(admin.TabularInline):
    model = InventoryChange
    extra = 0
    readonly_fields = ('change_type', 'quantity_changed', 'changed_by', 'change_date')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'price', 'sku', 'category', 'date_added', 'managed_by']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'date_added']
    ordering = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
