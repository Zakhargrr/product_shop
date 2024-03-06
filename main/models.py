from django.db import models

from config import settings


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='наименование')
    slug = models.CharField(max_length=32, verbose_name='slug')
    image = models.ImageField(upload_to='cat_images/', verbose_name='изоборажение')

    def __str__(self):
        return f"{self.name} ({self.slug})"

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Subcategory(models.Model):
    name = models.CharField(max_length=32, verbose_name='наименование')
    slug = models.CharField(max_length=32, verbose_name='slug')
    image = models.ImageField(upload_to='subcat_images/', verbose_name='изоборажение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')

    def __str__(self):
        return f"{self.name} ({self.slug})"

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'подкатегории'


class Product(models.Model):
    name = models.CharField(max_length=32, verbose_name='наименование')
    slug = models.CharField(max_length=32, verbose_name='slug')
    big_image = models.ImageField(upload_to='product_images/', verbose_name='большое изоборажение')
    middle_image = models.ImageField(upload_to='product_images/', verbose_name='среднее изоборажение')
    small_image = models.ImageField(upload_to='product_images/', verbose_name='маленькое изоборажение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, editable=False, verbose_name='категория')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='подкатегория')
    price = models.FloatField(verbose_name='цена')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class BasketProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    amount = models.IntegerField(verbose_name='количество')

    class Meta:
        verbose_name = 'продукт в корзине'
        verbose_name_plural = 'продукты в корзине'


class Basket(models.Model):
    products = models.ManyToManyField(BasketProduct, verbose_name='продукты')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'
