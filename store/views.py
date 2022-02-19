from django.shortcuts import get_object_or_404, render
from store.models import *
from store.forms import *
from django.core.mail import send_mail
from django.contrib import messages
from Ecommerce_Project import settings
from django.http import JsonResponse
import json
import requests
import datetime as dt
from .utils import cookie_cart


#from django.views.generic.detail import DetailView


# Create your views here.


def home(request):
    """If not exists an order, create a new one everytime the home url is request. Also, only get the orders when complete is False, if a order is complete=True, 
    the order does'nt shows and create a new one. """

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        cookie_data = cookie_cart(request)
        order = cookie_data['order']

    products = Product.objects.all().order_by("name")

    context = {"products": products, "order": order, "shipping": False}
    return render(request, 'store/home.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        # Items is access to all the order items in that order. Father class= Order. Child Class= Product_Order (order detail).
        items = order.product_order_set.all()

    # Guest User
    else:
        cookie_data = cookie_cart(request)
        order = cookie_data['order']
        items = cookie_data['items']

    context = {"items": items, "order": order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        # Items is access to all the order items in that order. Father class= Order. Child Class= Product_Order (order detail).
        items = order.product_order_set.all()
    else:
        cookie_data = cookie_cart(request)
        order = cookie_data['order']
        items = cookie_data['items']

    context = {"items": items, "order": order, "shipping": False}
    return render(request, 'store/checkout.html', context)


def product_detail(request, slug):
    product_detail = get_object_or_404(Product, slug=slug)
    product_detail.view_count += 1
    product_detail.save()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        cookie_data = cookie_cart(request)
        order = cookie_data['order']

    context = {'product': product_detail, "order": order}
    return render(request, 'store/productdetail.html', context)


"""
class ProductDetailView(DetailView):
    model = Product
    template_name = "store/productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs["slug"]
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context["product"] = product
        return context
"""


def update_item(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('Action:', action, 'ProductID: ', productID)

    customer = request.user.customer
    # Get a single product by id.
    product = Product.objects.get(id=productID)
    # Get or create if not exists the order for the customer.
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    # Get or create, if exists an order, change the value of quantity of the productid.
    orderItem, created = Product_Order.objects.get_or_create(
        order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def process_order(request):
    print('Data:', request.body)
    transaction_id = dt.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        total = data['form']['total']
        order.transaction_id = transaction_id

        if int(total) == int(order.get_cart_total):
            order.complete = True
            order.save()

        if order.shipping == True:
            Shipping_Address.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print("User is not logged in...")
    return JsonResponse('Payment complete', safe=False)


def contact_us(request):
    f = ContactForm(request.POST)
    if f.is_valid():
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {"secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response}
        url = 'https://www.google.com/recaptcha/api/siteverify'
        r = requests.post(url=url, data=data)
        result = r.json()
        # r= codigo de respuesta. Result= la respuesta json del post a googlecaptcha.
        print(result)
        # f contiene toda la data sin limpiar del formulario, con las etiquetas html de tabla, label, input type, etc.
        print(f)

        # Si el captcha es valido, es decir, si success es igual a true.
        if result['success']:
            # cleaned data rescata los datos ingresados por usuario en formulario en forma de diccionario.
            infoForm = f.cleaned_data
            send_mail(infoForm["subject"], infoForm["message"] + "\n " + str(infoForm["phone_number"]) + "\n " + infoForm["email"],
                      infoForm["email"], ["snaker.extreme.15@gmail.com"],)
            messages.success(request, "Gracias por contactarnos.")

            # Se reinicia f para limpiar campos, por lo que cuando se hace la request a la pagina, inicialmente es de tipo get, para renderizar en contactov2 el contenido de f(campos), y el captcha.
            # Luego, si la request es de tipo post, es decir, se rellanan campos, se hace click en enviar, se ejecuta todo el contenido del IF.
            f = ContactForm()
        else:
            messages.error(request, "Haz click en la casilla para continuar")
    else:
        result = ""

    return render(request, "store/contact.html", {"form": f, "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY, "result": result})
