from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, get_connection
from django.contrib import messages
from shop.views import filter_func
from shop.models import Shoes, Images

# Create your views here.
def home(request):
    items = filter_func("recent", items=Shoes.objects.all())
    items = items[:5]
    images_url = []
    for item in items:
        img_id = item.auto_increment_id
        images_url.append(Images.objects.filter(img_id=img_id)[0].images.url)
        print(Images.objects.filter(img_id=img_id)[0].img_id.title)
    items = zip(items, images_url)
    context = {"items": items}
    return render(request, 'home/base.html', context)

def social_media(request):
    return render(request, "home/social_media.html")

def contact(request):

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            con = get_connection("django.core.mail.backends.smtp.EmailBackend")
            send_mail(
                data.get("subject"),
                data.get("message") + f"\n\nEmail from {data.get('email')}",
                "sneakershopresetpw@gmail.com",
                ["sneakershopresetpw@gmail.com"],
                con
            )
            messages.success(request, "the message has been sent")
            return redirect("contact")
    else:
        form = ContactForm()
        if request.user.is_authenticated:
            values = {"user": request.user}
            form = ContactForm(initial=values)

    return render(request, "home/contact.html", context={"form": form})
