import pytest
from django.test import TestCase
from cart.models import Cart, CartItem
from users.models import CustomUser
from e_shop.models import Product, Category
from decimal import Decimal


@pytest.mark.django_db
class CartModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.force_login(self.user)
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="Phones", slug="phones")
        self.product_1 = Product.objects.create(
            category=self.category,
            title="iPhone 16",
            brand="Apple",
            description="Latest iPhone model",
            price=999.99,
            slug="iphone-16"
        )
        self.product_2 = Product.objects.create(
            category=self.category,
            title="iPhone 15",
            brand="Apple",
            description="15th iPhone model",
            price=899.99,
            slug="iphone-15"
        )

    def test_cart_str(self):
        self.assertEqual(str(self.cart), f'Cart admin')

    def test_get_total_price_empty(self):
        self.assertEqual(self.cart.get_total_price(), 0)

    def test_get_total_price_full(self):
        CartItem.objects.create(cart=self.cart, product=self.product_1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product_2, quantity=3)
        self.assertEqual(self.cart.get_total_price(), Decimal('4699.95'))

    def test_get_cart_items_empty(self):
        self.assertEqual(self.cart.get_cart_items(), '')

    def test_get_cart_items_full(self):
        CartItem.objects.create(cart=self.cart, product=self.product_1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product_2, quantity=3)
        self.assertEqual(
            self.cart.get_cart_items(),
            "iPhone 16: 2 x 999.99 = 1999.98, iPhone 15: 3 x 899.99 = 2699.97"
        )

@pytest.mark.django_db
class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.force_login(self.user)
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="Phones", slug="phones")
        self.product_1 = Product.objects.create(
            category=self.category,
            title="iPhone 16",
            brand="Apple",
            description="Latest iPhone model",
            price=999.99,
            slug="iphone-16"
        )
        self.product_2 = Product.objects.create(
            category=self.category,
            title="iPhone 15",
            brand="Apple",
            description="15th iPhone model",
            price=899.99,
            slug="iphone-15"
        )
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product_1, quantity=2)

    def test_cart_item_str(self):
        self.assertEqual(str(self.cart_item), f"2 x iPhone 16")

    def test_total_price(self):
        self.assertEqual(self.cart_item.total_price(), 1999.98)

    def test_cart(self):
        self.assertEqual(self.cart_item.cart, self.cart)

    def test_cart_product(self):
        self.assertEqual(self.cart_item.product, self.product_1)

    def test_cart_quantity(self):
        self.assertEqual(self.cart_item.quantity, 2)
