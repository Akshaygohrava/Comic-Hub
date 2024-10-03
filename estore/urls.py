"""estore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("storem/", views.storem, name="storem"),
    path("storem/", views.storem, name="storem"),
    path("cartview/", views.cartview, name="cartview"),
    path("login", views.hlogin, name="login"),
    path("logout", views.hlogout, name="logout"),
    path("register", views.register, name="register"),
    path("removefromcart/", views.removefromcart, name="removefromcart"),
    path("checkout/", views.checkout, name="checkout"),
    path("completeorder/", views.completeorder, name="completeorder"),
    path("about/", views.about, name="about"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
