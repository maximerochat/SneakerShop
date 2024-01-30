from django import template
from django.core.paginator import Paginator

from shop.models import Shoes
register = template.Library()


@register.filter
def list_index(indexable):
    # print(list(len(indexable)))
    return range(len(indexable))


@register.filter
def get_cart_num(instance):
    return instance.cart_set.all()[0].items.all().count()


@register.filter
def add_tva(total):
    return round(total + 0.074 * total, 2)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), None)


@register.filter
def get_item_filter_size(dictionary, key):
    return dictionary.get(str(key), False)


@register.filter
def times(number):
    return range(number)


@register.filter
def sum_json(dict):
    print(dict)
    var = 0
    for key, value in dict.items():
        print(value)
        var += float(value[0]) * int(value[1])
    return round(var, 2)


@register.filter
def to_str(input_):
    return str(input_)


@register.filter
def multiply(num1, num2):
    return float(num1)*float(num2)


@register.inclusion_tag('shop/recommendations.html', takes_context=True)
def recommendations(context):
    print(context)
    items = Shoes.objects.order_by("-auto_increment_id").exclude(auto_increment_id=context["item"].auto_increment_id)[:9]
    print(len(items))
    paginator = Paginator(items, 9)
    page = paginator.page(1)
    print(page.paginator.num_pages)
    context.update({"page": page})
    return context


@register.simple_tag
def define(val=None):
    return val


@register.filter
def get_higher_price(queryset):
    return queryset.order_by("-price").first().price

@register.filter
def to_int(value):
    return int(value)
