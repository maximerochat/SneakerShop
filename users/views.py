from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from verify_email.email_handler import send_verification_email
from payement.models import Order
from django.views.generic import ListView

from .forms import UserRegisterForm, UserUpdateForm
# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)

            messages.success(request, "Your account has been created! Please see your inbox to activate your account")
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", context={"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "You successfully updated your details")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, "users/profile.html", context={"form": u_form})



class OrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "users/orders_list.html"
    context_object_name = "items"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        qs = qs.filter(user=user).order_by("-order_id")
        print(qs)
        return qs

class OrderDetailView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "users/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        order_id = self.kwargs["id"]
        user = self.request.user
        qs = super().get_queryset()
        qs = qs.filter(user=user).filter(order_id=order_id).first()
        print(qs)
        return qs
