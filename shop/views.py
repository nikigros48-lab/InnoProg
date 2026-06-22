from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Product
import datetime


def all_products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    current_time = datetime.datetime.now()
    return render(
        request,
        "products.html",
        {"products": products, "current_time": current_time},
    )
