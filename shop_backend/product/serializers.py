from .models import Product, Color, Size, ProductImage, Category
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['id','name']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields=['id','name']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','name']


class ProductImage(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields=['id','image','is_main_image']


class ProductSerializer(serializers.ModelSerializer):

    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)
    image = ProductImage(many=True, source='images')
    
    class Meta:
        model=Product
        fields='__all__'

        

class ProductCreateSerializer(serializers.ModelSerializer):
    sizes = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(), many=True)
    colors = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), many=True)
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Product
        fields =  [
            'id', 'name', 'description', 'price', 'stock_quantity', 'discount',
            'discounted_price', 'category', 'styles', 'sizes', 'colors', 'images','rating'
        ]  # Specify fields required for product creation

        def create(self, validated_data):
            validated_data['user'] = self.context['request'].user   #associate user

            images= validated_data.pop('image')
            product=Product.objects.create(**validated_data)
            #create a product with remaining data

            # Iterate through the image objects to create an image
            for idx,image in enumerate(images):
                ProductImage.objects.create(product=product, image=image, is_main_image=(idx == 0))
            return Product

        # def create(self, validated_data):
        #     #automatically associate the login user with the product
        #     validated_data['user']=self.context['request'].user
        #     return super().create(validated_data)