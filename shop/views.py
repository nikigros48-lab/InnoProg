from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View

from .forms import UserAuthForm
from .models import Product
import datetime


def common_page(request: HttpRequest) -> HttpResponse:
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


class RegistrationView(View):

    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        form = UserCreationForm()
        return render(request, "registration.html", {"form": form})

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products")
        else:
            return render(request, "registration.html", {"form": form})


class LoginView(View):

    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        form = UserAuthForm()
        return render(request, "login.html", {"form": form})

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
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
