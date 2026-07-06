from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, DetailView
import json
from django.http import JsonResponse

from .forms import UserAuthForm
from .mixins import IsAuthenticatedMixin
from .models import Product
import datetime


def common_page(request: HttpRequest) -> HttpResponse:
    return render(request, "common.html", context={"request": request})


class AllProductsView(IsAuthenticatedMixin, ListView):
    model = Product
    template_name = "products.html"
    context_object_name = "products"
    extra_context = {"current_time": datetime.datetime.now()}


@method_decorator(ensure_csrf_cookie, name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related("productimage_set")


class CartView(View):

    def get(self, request):
        product_id = request.GET.get("product_id")
        if product_id:
            cart = request.session.get("cart", {})
            in_cart = str(product_id) in cart
            return JsonResponse({"in_cart": in_cart})

        cart = request.session.get("cart", {})
        return JsonResponse({"cart": cart})

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        product_id = data["product_id"]
        quantity = data["quantity"]
        cart = request.session.get("cart", {})

        if cart is None:
            cart = {}

        if str(product_id) not in cart:
            cart[str(product_id)] = quantity
        else:
            cart[str(product_id)] += quantity

        request.session.update({"cart": cart})

        return JsonResponse({"success": True})

    def delete(self, request, product_id: int):
        cart = request.session.get("cart", {})

        if cart is None:
            return JsonResponse({"detail": "Cart does not exist"}, status=400)

        if str(product_id) not in cart:
            return JsonResponse({"detail": "Product not in cart"}, status=400)

        del cart[str(product_id)]

        request.session.update({"cart": cart})
        return JsonResponse({}, status=204)


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
