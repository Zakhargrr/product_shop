from django.conf.urls.static import static
from django.urls import path

from config import settings
from main.apps import MainConfig
from main.views import CategoryListAPIView, ProductListAPIView, change_basket, retrieve_basket, clear_basket

app_name = MainConfig.name

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('products/', ProductListAPIView.as_view(), name='products'),
    path('change-basket/<int:product_pk>/', change_basket, name='change_basket'),
    path('my-basket/', retrieve_basket, name='retrieve_basket'),
    path('clear-basket/', clear_basket, name='clear_basket')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
