from django.contrib import admin
from store.models import Customer, Product, Order, Product_Order, Shipping_Address, Category
#from .models import *

# Register your models here.


class Customer_admin(admin.ModelAdmin):
    search_fields = ("user", "name", "email")


class Product_admin(admin.ModelAdmin):
    list_filter = ("digital", "price",)
    search_fields = ("name", "digital")


class Order_admin(admin.ModelAdmin):
    list_display = ("customer", "transaction_id", "date_ordered", "complete")
    list_filter = ("date_ordered", "complete")
    date_hierarchy = "date_ordered"
    list_per_page = 15


class Product_Order_Admin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "date")


class Shipping_Adress_admin(admin.ModelAdmin):
    list_filter = ("city",)


admin.site.register(Customer, Customer_admin)
admin.site.register(Product, Product_admin)
admin.site.register(Order, Order_admin)
admin.site.register(Product_Order, Product_Order_Admin)
admin.site.register(Shipping_Address, Shipping_Adress_admin)
admin.site.register(Category)
