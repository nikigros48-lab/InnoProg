from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Product

# Create your views here.
def all_products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return HttpResponse(f"<p>{product}</p>" for product in products)