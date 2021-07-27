from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session  # storing current session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:  # Checking if any cart is present
            cart = self.session[settings.CART_SESSION_ID] = {}  # creating an empty cart
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        # products = Product.objects.get(id__in=product_ids) Why did the book use get?!
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']  # getting total for price for each item
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        # return sum(Decimal(item['total_price']) for item in self.cart.values())  # Why do I get key error for total_price?
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def clear(self):  # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()



