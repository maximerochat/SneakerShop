from django.urls import path, include
from .views import CreateCheckoutSessionView, cancel_payment, success_payment, my_webhook_view

urlpatterns = [
    path("create-checkout-session/<cart_id>", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("cancel/", cancel_payment, name="cancel_payment"),
    path("success/", success_payment, name="success_payment"),
    path("webhooks/stripe/", my_webhook_view, name="stripe_webhook")
]