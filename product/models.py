from django.contrib.auth import get_user_model
from django.db import models

from user.models import MyUser

MyUser = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя категории', unique=True)
    slug = models.SlugField(primary_key=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products', blank=True, null=True, verbose_name='Изображение')
    additional_information = models.CharField(max_length=50, verbose_name='Вес в кг')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    country = models.CharField(max_length=255, verbose_name='Страна')

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Продукт')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} оставил комментарии на продукт {self.product}'


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)

