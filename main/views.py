from django.db import ProgrammingError
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Category, Product, Basket, BasketProduct
from main.paginators import CustomPaginator
from main.serializers import CategorySerializer, ProductSerializer
from main.service import Cart


# Create your views here.

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CustomPaginator


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPaginator


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        self.check_object_permissions(request, cart)
        return Response(
            {'data': request.session
             },
            status=status.HTTP_200_OK
        )
        return Response(
            {'data': list(iter(cart)),
             'cart_total_price': cart.get_total_price(),
             'cart_total_quantity': len(cart)
             },
            status=status.HTTP_200_OK
        )


    def post(self, request, **kwargs):
        cart = Cart(request)
        self.check_object_permissions(request, cart)

        if 'product_pk' not in request.data:
            return Response({'message': 'в теле запроса нет id продукта'}, status=status.HTTP_400_BAD_REQUEST)

        product_pk = request.data['product_pk']
        if not Product.objects.filter(pk=product_pk):
            return Response({'message': 'продукта с таким id не существует'}, status=status.HTTP_400_BAD_REQUEST)

        if 'remove' in request.data:
            cart.remove(product_pk)
            return Response({'message': 'товар убран из корзины'}, status=status.HTTP_202_ACCEPTED)

        elif 'add' in request.data:
            cart.add(product_pk=product_pk,
                     quantity=request.data[
                         "quantity"] if "quantity" in request.data else 1,
                     override_quantity=request.data[
                         "override_quantity"] if "override_quantity" in request.data else False
                     )
            return Response({'message': 'корзина обновлена'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': 'такое действие не предусмотрено'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart = Cart(request)
        cart.clear()

        return Response({'message': 'корзина очищена'}, status=status.HTTP_202_ACCEPTED)
