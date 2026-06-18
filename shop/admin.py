from django.contrib import admin
from shop.models import Product, Attribute
from shop.filters import StockFilter

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock')
    search_fields = ('title', 'description')
    list_filter = (StockFilter,)
    actions = ['reset_stock']

    @admin.action(description='Обнулить остатки')
    def reset_stock(self, request, queryset):
        queryset.update(stock=0)
        self.message_user(request, 'Остатки успешно обнулены!', 'success')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
