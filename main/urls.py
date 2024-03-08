from django.conf.urls.static import static
from django.urls import path

from config import settings
from main.apps import MainConfig
from main.views import CategoryListAPIView, ProductListAPIView, \
    CartAPIView

app_name = MainConfig.name

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('products/', ProductListAPIView.as_view(), name='products'),
    path('cart/', CartAPIView.as_view(), name='cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
