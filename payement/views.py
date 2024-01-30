from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.conf import settings
from users.models import Cart
from shop.models import Shoes
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from .models import Order
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        cart_id = self.kwargs.get("cart_id")
        YOUR_DOMAIN = "https://maximerochat.ch/payment/"
        cart = Cart.objects.filter(user_id=cart_id).first()
        list_items = []
        metadata = {}
        print(cart.items)
        i = 0
        # items_dict = {}
        for item in cart.items.all():
            i += 1

            items_dict = {
                "price_data": {
                      "currency": "chf",
                      "unit_amount": item.price_cents_tva,
                        "product_data": {
                            "name": item.title,
                        },
                    },
                    'quantity': cart.quantity.get(str(item.auto_increment_id)),
            }
            print(items_dict)
            metadata.update({f"product_{i}": f"{item.auto_increment_id}, {cart.quantity.get(str(item.auto_increment_id))}"})
            list_items.append(items_dict)
            print(item.title)
        metadata.update({"customer": f"{request.user.id}"})
        checkout_session = stripe.checkout.Session.create(
            line_items=list_items,
            metadata=metadata,
            mode='payment',
            success_url= f'{YOUR_DOMAIN}success/',
            cancel_url= f'{YOUR_DOMAIN}cancel/',
        )
        print(list_items)
        # return JsonResponse({
        #     "id": checkout_session.id
        # })
        return redirect(checkout_session.url)


def success_payment(request):
    messages.success(request, "Your payment has been accepted")
    return redirect("cart")


def cancel_payment(request):
    messages.warning(request, "Your paymment has been canceled")
    return redirect("home")


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    print(request.META)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        items_ids = session["metadata"]
        print(items_ids["product_1"].split(", ")[1])
        title_list = [Shoes.objects.filter(auto_increment_id=int(value[0])).first().title for key, value in items_ids.items() if key!="customer"]
        for key, value in items_ids.items():
            if key != "customer":

                shoes = Shoes.objects.filter(auto_increment_id=int(value.split(", ")[0])).first()
                if shoes.quantity >= int(value.split(", ")[1]):
                    shoes.quantity -= int(value.split(", ")[1])
                    shoes.save()
                else:
                    shoes.quantity = 0
                    shoes.save()
                print(key, value, "voila les key value de la shoes")


        # for relation in Cart.items.all()
        cart = Cart.objects.filter(user_id=int(items_ids["customer"])).first()
        cart.items.clear()
        cart.quantity = {}
        cart.save()

        dict_order = {Shoes.objects.filter(auto_increment_id=int(value.split(", ")[0])).first().title:
                      [Shoes.objects.filter(auto_increment_id=int(value.split(", ")[0])).first().price_tva, int(value.split(", ")[1])]
                      for key, value in items_ids.items() if key!="customer"}
        print(items_ids)
        print("cutomer =        ", items_ids["customer"])
        print(dict_order)
        order = Order.objects.create(items=dict_order, user=User.objects.filter(id=int(items_ids["customer"])).first())
        # order.user.add(User.objects.filter(id=int(items_ids["customer"])).first())

        html_message = loader.render_to_string(
            'payment/email_receipt.html',
            {
                'title_list': title_list
            }
        )
        send_mail(
            subject="Here is your product",
            message="thanks for your puchase.",
            recipient_list=[customer_email],
            from_email="sneakershopresetpw@gmail.com",
            html_message=html_message
        )
        print("email sent")
    # Passed signature verification
    return HttpResponse(status=200)


class ProductLandingPage(TemplateView):
    template_name = "payment/checkout.html"

    def get_context_data(self, **kwargs):
        context = super(ProductLandingPage, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_SECRET_KEY
        })
