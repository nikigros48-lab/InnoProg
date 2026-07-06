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
        if cart is None:
            return JsonResponse({"error": "Корзина не найдена"}, status=404)
        return JsonResponse({"cart": cart})

    def post(self, request):
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
        else:
            data = request.POST

        product_id = str(data.get("productId") or data.get("product_id"))
        if not product_id:
            return JsonResponse({"error": "productId required"}, status=400)

        try:
            quantity = int(data.get("quantity", 1))
        except (ValueError, TypeError):
            return JsonResponse({"error": "Quantity must be integer"}, status=400)

        if quantity < 1:
            return JsonResponse({"error": "Quantity must be positive"}, status=400)

        cart = request.session.get("cart", {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session["cart"] = cart
        request.session.modified = True
        return JsonResponse({"success": True, "cart": cart})

    def delete(self, request):
        try:
            data = json.loads(request.body)
            product_id = str(data["productId"])
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"error": "Invalid data"}, status=400)

        cart = request.session.get("cart", {})
        if product_id in cart:
            del cart[product_id]
            request.session["cart"] = cart
            request.session.modified = True
        return JsonResponse({"success": True, "cart": cart})


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
