from django.urls import path
from .views import home, social_media, contact
from shop.views import shop

urlpatterns = [
    path('', home, name='home'),
    path("social-media", social_media, name="social_media"),
    path("contact/", contact, name="contact")
]