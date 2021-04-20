from django.db import models

from be_healthy.product.models import Product, User


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product', verbose_name='продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='Пользователь')
    price = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Цена')
    final_price = models.CharField(max_length=255)

