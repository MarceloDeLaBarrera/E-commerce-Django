import json
from .models import *


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print(cart)
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0, 'shipping': False}

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
