from django.conf import settings
from django.db import models

from e_shop.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of create')

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f'Cart {self.user}'

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.cart_items.all())

    def get_cart_items(self):

        return ', '.join([f"{item.product.title}: {item.quantity} x {item.product.price} = {item.total_price()}" for item in self.cart_items.all()])


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return 0 + (self.product.price * self.quantity)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
