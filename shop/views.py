from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserAuthForm
from .models import Product
import datetime


def common_page(request: HttpRequest) -> HttpResponse:
    is_authenticated = request.user.is_authenticated
    return render(request, "common.html", context={"request": request})


def all_products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    current_time = datetime.datetime.now()
    return render(
        request,
        "products.html",
        {
            "products": products,
            "current_time": current_time,
        },
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


def login_page(request: HttpRequest) -> HttpResponse:
    form = UserAuthForm()
    if request.method == "POST":
        form = UserAuthForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("products")
            else:
                messages.error(request, "Username or password is incorrect")
    return render(request, "login.html", {"form": form})


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("products")
