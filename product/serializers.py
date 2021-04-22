from rest_framework import serializers
from rest_framework.decorators import action

from .models import *


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(CategoryDetailSerializer, self).to_representation(instance)
        return representation


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    created = serializers.DateTimeField(format='%d %B %Y %H:%M', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        action = self.context.get('action')
        reviews = ReviewSerializer(instance.reviews.all(), many=True).data
        print(self.context.get('view').__dict__.get('action'))
        likes = LikeSerializer(instance.likes.filter(like=True), many=True).data
        if self.context.get('view').__dict__.get('action') == 'list':
            representation['reviews'] = len(reviews)
            representation['likes'] = len(likes)
        if self.context.get('view').__dict__.get('action') == 'retrieve':
            representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
            representation['likes'] = LikeSerializer(instance.likes.filter(like=True), many=True).data
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Review
        fields = ('product', 'body', )

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        review = Review.objects.create(user=author, **validated_data)
        return review

    def to_representation(self, instance):
        representation = super(ReviewSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        return representation


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     favourite = Favorite.objects.create(user=user, **validated_data)
    #     return favourite

    def to_representation(self, instance):
        representation = super(FavoriteSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        return representation

