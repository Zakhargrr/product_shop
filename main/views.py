from django.db import ProgrammingError
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Category, Product, Basket, BasketProduct
from main.paginators import CustomPaginator
from main.serializers import CategorySerializer, ProductSerializer


# Create your views here.

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CustomPaginator


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPaginator


@api_view(['POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def change_basket(request, product_pk):
    valid_product = Product.objects.filter(pk=product_pk)

    if not valid_product:
        message = {'message': 'продукта с таким id не существует'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    valid_product = valid_product[0]
    user = request.user
    owner_basket = Basket.objects.filter(owner=user.id)
    if not owner_basket:
        owner_basket = [Basket.objects.create(owner=user)]

    if request.method == 'POST':
        try:
            amount = request.data['amount']
        except KeyError:
            amount = 1

        existing_product = owner_basket[0].products.filter(product=product_pk)
        if not existing_product:
            basket_product = BasketProduct.objects.create(
                product=valid_product,
                amount=amount
            )
            owner_basket[0].products.add(basket_product)
            message = {'message': 'продукт добавлен в корзину'}
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {'message': 'продукт уже есть в корзине'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            amount = request.data['amount']
        except KeyError:
            amount = 1
        existing_product = owner_basket[0].products.filter(product=product_pk)
        if not existing_product:
            message = {'message': 'продукт еще не добавлен в корзину'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            existing_product[0].amount = amount
            existing_product[0].save()
            message = {'message': 'количество продукта изменено'}
            return Response(message, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        existing_product = owner_basket[0].products.filter(product=product_pk)
        if not existing_product:
            message = {'message': 'продукт еще не добавлен в корзину'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            existing_product[0].delete()
            message = {'message': 'продукт удален из корзины'}
            return Response(message, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_basket(request):
    user = request.user
    owner_basket = Basket.objects.filter(owner=user.id)
    if not owner_basket:
        message = {'message': 'корзина пуста'}
        return Response(message, status=status.HTTP_200_OK)
    else:
        products_arr = []
        total_price = 0
        total_amount = 0
        for basket_product in owner_basket[0].products.all():
            product_dict = {'product': str(basket_product.product),
                            'price': basket_product.product.price,
                            'amount': basket_product.amount}
            products_arr.append(product_dict)
            total_amount += basket_product.amount
            total_price += basket_product.amount * basket_product.product.price
        response = {
            'products': products_arr,
            'total_amount': total_amount,
            'total_price': total_price
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_basket(request):
    user = request.user
    owner_basket = Basket.objects.filter(owner=user.id)
    if not owner_basket:
        message = {'message': 'корзина пуста'}
        return Response(message, status=status.HTTP_200_OK)
    else:
        owner_basket[0].delete()
        message = {'message': 'корзина очищена'}
        return Response(message, status=status.HTTP_200_OK)
