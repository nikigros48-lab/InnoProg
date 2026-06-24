from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm
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


def registration_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products")
        else:
            return render(request, "registration.html", {"form": form})
    form = UserCreationForm()
    return render(request, "registration.html", {"form": form})
