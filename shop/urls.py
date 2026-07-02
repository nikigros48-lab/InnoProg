from django.urls import path
from .views import AllProductsView, ProductDetailView

urlpatterns = [
    path("products/", AllProductsView.as_view(), name="products"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]
