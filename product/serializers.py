from rest_framework import serializers
from .models import *
from .views import Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    created = serializers.DateTimeField(format='%d %B %Y %H:%M', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        problem = Product.objects.create(**validated_data)
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        review = Review.objects.create(author=author, **validated_data)
        return review


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('title', 'price', 'final_price', 'quantity')
