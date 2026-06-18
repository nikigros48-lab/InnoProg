from django.contrib.admin import SimpleListFilter

class ProductStockFilter(SimpleListFilter):
    title = 'Наличие на складе'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return (
            ('in_stock', 'В наличии'),
            ('out_of_stock', 'Нет в наличии'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'in_stock':
            return queryset.filter(stock__gt=0)
        elif self.value() == 'out_of_stock':
            return queryset.filter(stock__lte=0)