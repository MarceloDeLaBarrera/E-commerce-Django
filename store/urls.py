from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("product/<slug:slug>/", views.product_detail, name="product-detail"),
    #path("product/<slug:slug>/",views.ProductDetailView.as_view(), name="product-detail"),
    path("update_item/", views.update_item, name="update-item"),
    path("contact-us/", views.contact_us, name="contact"),

]
