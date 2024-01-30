from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Shoes, Images, Option
from users.models import Cart


def filter_func(filter, items):
    if filter == "recent":
        return items.order_by("-auto_increment_id")
    elif filter == "pricedesc":
        return items.order_by("-price")

    elif filter == "priceasc":
        return items.order_by("price")



# Create your views here.
def base(request, filter):
    if filter == "recent":
        items = Shoes.objects.all().order_by("-auto_increment_id")[:5]
    elif filter == "pricedesc":
        items = Shoes.objects.all().order_by("-price")[:5]
    elif filter == "priceasc":
        items = Shoes.objects.all().order_by("price")[:5]

    images_url = []

    for item in items:
        img_id = item.auto_increment_id
        images_url.append(Images.objects.filter(img_id=img_id)[0].images.url)
    items = zip(items, images_url)
    context = {"items": items}
    return render(request, "shop/article.html", context)

def product_view(request, id, filter=None):

    item = Shoes.objects.filter(auto_increment_id=id)
    images = Images.objects.filter(img_id=id)

    # if request.method == "POST":
    #     if

    if len(item) > 0:
        context = {"item": item[0],
                   "images": images}

        return render(request, "shop/product.html", context=context)
    items = Shoes.objects.all().order_by("-auto_increment_id")[:5]
    images_url = []
    for item in items:
        img_id = item.auto_increment_id
        images_url.append(Images.objects.filter(img_id=img_id)[0].images.url)
    items = zip(items, images_url)
    return render(request, "shop/not_found_error.html", context={ "items" : items })


def redirect_view(request):
    return redirect("shop-1", page=1)

def search_view(request, search_input, filter=None):
    items = Shoes.objects.all().filter(title__contains=search_input)
    if filter is not None:
        items = filter_func(filter=filter, items=items)
    images_url = []
    no_result = False
    if len(items) == 0:
        items = Shoes.objects.all()[:5]
        no_result = True
    #     return render(request, "shop/not_found_error.html", context={"items": items})
    for item in items:

        img_id = item.auto_increment_id
        images_url.append(Images.objects.filter(img_id=img_id)[0].images.url)
        print(Images.objects.filter(img_id=img_id)[0].img_id.title)
    items = zip(items, images_url)
    context = {"items": items}
    if no_result:
        return render(request, "shop/not_found_error.html", context)
    return render(request, "shop/search.html", context)

def buy_view(request, id):
    return render(request, "shop/buy.html")

def redirect_filter_search_view(request, search_input, filter):
    return redirect("search_view", search_input=search_input, filter=filter)

def redirect_shop(request):
    print("redurect")
    return redirect("shop", filter="recent", page=1)

def shop(request, filter, page):
    filters = filter.split("?")
    # if "search_input" in filters:
    print(request.GET.get("test"))
        # print(filters.index("search_input"))
        # search_input =
    search_input = ""
    if filter == "recent":
        items = Shoes.objects.all().order_by("-auto_increment_id")
    elif filter == "pricedesc":
        items = Shoes.objects.all().order_by("-price")

    elif filter == "priceasc":
        items = Shoes.objects.all().order_by("price")
    else:
        items = Shoes.objects.all().filter(title__contains=filter)
        search_input = filter
    # items = filter_func(filter, items=Shoes.objects.all())
    paginator = Paginator(items, 9)
    page_el = paginator.page(page)
    images_url = []
    for item in page_el:
        img_id = item.auto_increment_id
        images_url.append(Images.objects.filter(img_id=img_id)[0].images.url)
        print(Images.objects.filter(img_id=img_id)[0].img_id.title)

    items = zip(page_el, images_url)
    context = {"items": items, "page_obj": page_el, "filter": filter, "search_input": search_input}
    return render(request, "shop/shop.html", context)


def shop_1(request, page=1):
    items = Shoes.objects.all()
    max_price = items.order_by("-price").first().price
    print(request.GET)
    filter = "?"

    filters_dict = {}
    search_input = request.GET.get("search_input", None)
    if search_input is not None:
        print(search_input)
        items = items.filter(title__contains=search_input)
        filter += f"search_input={search_input}&"
        filters_dict["search_input"] = search_input
        if len(items) == 0:
            items = Shoes.objects.all().order_by("-auto_increment_id")[:5]
            images_url = []
            for item in items:
                img_id = item.auto_increment_id
                images_url.append(Images.objects.filter(img_id=img_id)[0].images.url)
            items = zip(items, images_url)
            return render(request, "shop/not_found_error.html", {"items": items})
    if request.GET.get("recent", None) is not None:
        filter += "recent"
        filters_dict["ordering"] = "recent"
        items = items.order_by("-auto_increment_id")
    elif request.GET.get("priceasc", None) is not None:
        filter += "priceasc"
        items = items.order_by("price")
        filters_dict["ordering"] = "priceasc"
    elif request.GET.get("pricedesc", None) is not None:
        filters_dict["ordering"] = "pricedesc"
        filter += "pricedesc"
        items = items.order_by("-price")

    if request.GET.get("min") is not None:
        items = items.filter(price__gte=float(request.GET.get("min")))
        filters_dict["min"] = request.GET.get("min")
        filter += f"&min={request.GET.get('min')}"
    if request.GET.get("max") is not None:
        items = items.filter(price__lte=float(request.GET.get("max")))
        filters_dict["max"] = request.GET.get("max")
        filter += f"&max={request.GET.get('max')}"

    if request.GET.get("brand") is not None:
        items = items.filter(id_brand__option__exact=request.GET.get("brand"))
        filters_dict["brand"] = request.GET.get("brand")
        filter += f"&brand={request.GET.get('brand')}"

    size_range1_key = "35-40"
    size_range2_key = "40-43"
    size_range3_key = "43-47"
    size_range1 = {size_range1_key: request.GET.get("35-40")}
    size_range2 = {size_range2_key: request.GET.get("40-43")}
    size_range3 = {size_range3_key: request.GET.get("43-47")}
    size_range = size_range1 | size_range2 | size_range3
    if size_range1[size_range1_key] is not None:
        # if  size_range1[size_range1_key] == "True":
        #     items = items.filter(size__range=(35, 40))
        filters_dict |= size_range1
        filter += f"&35-40={size_range1[size_range1_key]}"
    if size_range2[size_range2_key] is not None:
        # if size_range2 == "True":
        #     items = items.filter(size__range=(40, 43))
        filters_dict |= size_range2
        filter += f"&40-43={size_range2[size_range2_key]}"
    if size_range3[size_range3_key] is not None:
        # if size_range3 == "True":
        #     items = items.filter(size__range=(43, 47))
        filters_dict |= size_range3
        filter += f"&43-47={size_range3[size_range3_key]}"

    keys_size_range = [key for key in size_range if size_range[key] == "True"]
    if len(keys_size_range) > 0:
        keys_size_range = "-".join(keys_size_range).split("-")
        keys_size_range = list(map(int, keys_size_range))
        print(keys_size_range)
        items = items.filter(size__range=(min(keys_size_range), max(keys_size_range)))


    paginator = Paginator(items, 9)
    page_el = paginator.page(page)
    images_url = []
    choices = [option.option for option in Option.objects.all()]
    for item in page_el:
        img_id = item.auto_increment_id
        images_url.append(Images.objects.filter(img_id=img_id)[0].images.url)
        print(Images.objects.filter(img_id=img_id)[0].img_id.title)
    items_zip = zip(page_el, images_url)
    print(filter)
    context = {"items": items_zip, "page_obj": page_el, "filter": filter, "filters": filters_dict , "search_input": search_input, "max_price": max_price, "CHOICES": choices}
    return render(request, "shop/shop.html", context)



@login_required
def add_cart_request(request, id_item):
    instance_cart = Cart.objects.filter(user_id=request.user).first()
    print(type(id_item))
    print(id_item)
    print(instance_cart.quantity)

    if str(id_item) not in instance_cart.quantity:
        instance_cart.quantity[str(id_item)] = 1
    else:
        instance_cart.quantity[str(id_item)] += 1
    instance_cart.items.add(Shoes.objects.filter(auto_increment_id=id_item)[0])
    instance_cart.save()
    print(instance_cart.quantity)
    return redirect("product", id=id_item)


@login_required
def add_cart_quantity(request, id_item, quantity):
    cart = Cart.objects.filter(user_id=request.user).first()
    print(id_item, quantity)
    cart.quantity[str(id_item)] = int(quantity)
    cart.save()
    return redirect("cart")


@login_required
def delete_cart_request(request, id):
    cart = Cart.objects.filter(user_id=request.user)[0]
    cart.items.remove(Shoes.objects.filter(auto_increment_id=id)[0])
    cart.quantity.pop(str(id))
    cart.save()
    print(id)
    print(cart)
    return redirect("cart")

def test(request):
    return render(request, "users/confirmation_mail_template.html")

class CartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = "shop/cart.html"
    context_object_name = "items"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        qs = qs.filter(user_id=user)
        return qs

# class ProductListView(ListView):
#     model = Shoes
#     template_name = "shop/article_list.html"
#     context_object_name = "items"
#     ordering = ["-auto_increment_id"]
#     p = -1
#     items = []
#     for i in range(len(Shoes.objects.all())):
#         items += Shoes.objects.prefetch_related("images_set").all()[i].images_set.all()
#     urls = []
#     print(items)
#     for item in items:
#         print(item.img_id)
#         print(p)
#         if p != item.img_id:
#             urls.append(item.images.url)
#         p = item.img_id
#
#     print(urls)
#     extra_context = {"urls": urls}
#     # def get(self,request, *args):
#     #     print(filter)
#     #     return render(request, self.template_name)

