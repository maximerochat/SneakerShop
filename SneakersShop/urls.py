"""SneakersShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from home.urls import urlpatterns as home_urls
from shop.urls import urlpatterns as shop_urls
from users.urls import urlpatterns as users_urls
from payement.urls import urlpatterns as payment_urls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path("", include(home_urls)),
    path("shop/", include(shop_urls)),
    path("", include(users_urls)),
    path('verification/', include('verify_email.urls')),
    path('accounts/', include('allauth.urls')),
    path("payment/", include(payment_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)