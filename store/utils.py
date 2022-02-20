import json
from .models import *


def cookie_cart(request):

    try:
        # Access to the content of the cart from cookies.
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print(cart)
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0, 'shipping': False}

    # Create a list with all the info of the items from guest user, to render them on cart and checkot.
    for item in cart:
        try:
            product = Product.objects.get(id=item)

            if product.offer_price:
                total = product.offer_price*cart[item]['quantity']
            else:
                total = product.price*cart[item]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[item]['quantity']
            product_item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'offer_price': product.offer_price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[item]['quantity'],
                'get_subtotal': total
            }
            items.append(product_item)

            if product.digital == False:
                order['shipping'] = True

        except:
            pass
    return{'order': order, 'items': items}


def cart_data(request):
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

    return{'order': order, 'items': items}


def guest_order(request, data):

    print("User is not logged in...")
    print("Cookies: ", request.COOKIES)

    name = data["form"]["name"]
    email = data["form"]["email"]
    cookie_data = cookie_cart(request)
    items = cookie_data["items"]

    # Create customer for a guest user.
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    # Create an order for that customer.
    order = Order.objects.create(customer=customer, complete=False)

    # Create a order detail(product_order) for that order, getting the product id and quantity by iterating on the list of products from the cart.
    for item in items:
        product = Product.objects.get(id=item["product"]["id"])
        order_item = Product_Order.objects.create(
            product=product, order=order, quantity=item["quantity"])

    return customer, order
