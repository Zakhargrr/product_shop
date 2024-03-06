from rest_framework import serializers

from main.models import Subcategory, Category, Product


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug', 'image']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(source='subcategory_set', many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategories']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()

    def get_images(self, instance):
        images = [{'big_image': self.context['request'].build_absolute_uri(instance.big_image.url)},
                  {'middle_image': self.context['request'].build_absolute_uri(instance.middle_image.url)},
                  {'small_image': self.context['request'].build_absolute_uri(instance.small_image.url)}]
        return images

    def get_category(self, instance):
        return str(instance.category)

    def get_subcategory(self, instance):
        return str(instance.subcategory)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'subcategory', 'price', 'images']
