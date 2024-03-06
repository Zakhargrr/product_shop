from django.contrib import admin

from main.models import Category, Subcategory, Product


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image', 'category')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'subcategory', 'big_image', 'middle_image', 'small_image', 'price')

    def save_model(self, request, obj, form, change):
        obj.category = obj.subcategory.category
        super().save_model(request, obj, form, change)
