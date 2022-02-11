from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, max_length=200, null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    price = models.IntegerField()
    offer_price = models.IntegerField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=1)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_ur1(self):
        return reverse("store:product-detail", kwargs={'slug': self.slug})

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.product_order_set.all()
        total = sum([item.get_subtotal for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.product_order_set.all()
        total = sum([item.quantity for item in order_items])
        return total


# Order detail -OrderItem
class Product_Order(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_subtotal(self):
        subtotal = 0
        if self.product.offer_price:
            subtotal = self.quantity*self.product.offer_price
        else:
            subtotal = self.quantity * self.product.price
        return subtotal


class Shipping_Address(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
