from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from shop.views import (
    logout_user,
    common_page,
    RegistrationView,
    LoginView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", common_page, name="home"),
    path("register/", RegistrationView.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("", include("shop.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
