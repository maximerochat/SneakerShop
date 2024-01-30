from django.urls import path

from .views import (
    base,
    product_view,
    redirect_view,
    search_view,
    buy_view,
    redirect_filter_search_view,
    shop,
    redirect_shop,
    add_cart_request,
    CartView,
    delete_cart_request,
    test,
    shop_1,
    add_cart_quantity,
    # ProductListView
)

urlpatterns = [
    path("", redirect_view, name="redirect-base"),

    path("products/<int:id>/", product_view, name="product"),

    path("", redirect_shop, name="redirect_shop"),

    path("<int:page>/", shop_1, name="shop-1"),
    path("products/<int:id_item>/add/", add_cart_request, name="add_cart_request"),
    path("add/<id_item>/<quantity>/", add_cart_quantity ,name="add_cart_quantity"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/delete/<int:id>", delete_cart_request, name="delete_cart_request"),
    path("test/", test)
]