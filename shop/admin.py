from django.contrib import admin
from shop.models import Product, Attribute, ProductImage
from shop.filters import ProductStockFilter


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "stock")
    search_fields = ("title", "description")
    list_filter = (ProductStockFilter,)
    actions = ["reset_stock"]

    @admin.action(description="Обнулить остатки")
    def reset_stock(self, request, queryset):
        queryset.update(stock=0)
        self.message_user(request, "Остатки успешно обнулены!", "success")


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "product")
