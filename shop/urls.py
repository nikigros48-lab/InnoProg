from django.urls import path
from .views import all_products, registration_view

urlpatterns = [
    path("products/", all_products, name="products"),
    path("register/", registration_view),
]
