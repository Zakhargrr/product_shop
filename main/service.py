from rest_framework import status
from rest_framework.response import Response

from config import settings
from main.models import Product
from main.serializers import ProductCartSerializer


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID]= {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product_pk, quantity=1, override_quantity=False):
        product = Product.objects.get(pk=product_pk)
        product_pk = str(product_pk)
        # valid_product = Product.objects.filter(pk=product_pk)
        # if not valid_product:
        #     message = {'message': 'продукта с таким id не существует'}
        #     return Response(message, status=status.HTTP_400_BAD_REQUEST)
        if product_pk not in self.cart:
            self.cart[product_pk] = {
                'quantity': 0,
                'price': product.price
            }
        if override_quantity:
            self.cart[product_pk]['quantity'] = quantity
        else:
            self.cart[product_pk]['quantity'] += quantity
        self.save()

    def remove(self, product_pk):
        product_pk = str(product_pk)
        if product_pk in self.cart:
            del self.cart[product_pk]
            self.save()

    def __iter__(self):
        product_pks = self.cart.keys()
        products = Product.objects.filter(id__in=product_pks)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.pk)]['product'] = ProductCartSerializer(product).data
        for item in cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(item["price"] * item["quantity"] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
