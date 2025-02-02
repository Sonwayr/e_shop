import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from e_shop.models import Category, Product
from users.models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from decimal import Decimal
from cart.models import Cart, CartItem
from django.urls import reverse

USER_MODEL = get_user_model()


@pytest.mark.django_db
class AddToCartViewTest(TestCase):

    def setUp(self):
        self.user = USER_MODEL.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            title="iPhone 16",
            slug="iphone-16",
            category=self.category,
            price=Decimal('999.99'),
            description="Latest iPhone model"
        )

        self.url_add_to_cart_1 = reverse('cart:add_to_cart', kwargs={'product_id': self.product.id, 'quantity': 1})
        self.url_add_to_cart_5 = reverse('cart:add_to_cart', kwargs={'product_id': self.product.id, 'quantity': 5})
        self.url_missing_quantity = f'/cart/add_to_cart/{self.product.id}/'
        self.url_missing_product_id = f'/cart/add_to_cart/?quantity=1/'

    def test_add_to_cart_redirects(self):
        """Test that add_to_cart redirects to the main page"""

        urls = [
            self.url_add_to_cart_1,
            self.url_add_to_cart_5,
            self.url_missing_quantity,
            self.url_missing_product_id,
        ]

        expected_status_codes = [
            status.HTTP_302_FOUND,
            status.HTTP_302_FOUND,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_404_NOT_FOUND,
        ]

        for url, expected_status_code in zip(urls, expected_status_codes):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status_code)
                if expected_status_code == status.HTTP_302_FOUND:
                    self.assertRedirects(response, reverse('e_shop:main_page'))

    def test_add_product_to_cart(self):
        response = self.client.get(self.url_add_to_cart_1)
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_existing_product_increases_quantity(self):
        response = self.client.get(self.url_add_to_cart_1)
        self.client.get(self.url_add_to_cart_1)
        cart_item = CartItem.objects.get(cart__user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_add_to_cart_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url_add_to_cart_1)
        self.assertEqual(response.status_code, 302)


@pytest.mark.django_db
class DeleteCartViewTest(TestCase):

    def setUp(self):
        self.user = USER_MODEL.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.cart = Cart.objects.create(user=self.user)
        self.url = reverse('cart:delete_cart')

    def test_delete_cart_redirect(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('e_shop:main_page'))

    def test_delete_cart(self):
        self.client.post(self.url)
        self.assertFalse(Cart.objects.filter(user=self.user).exists())

    def test_delete_cart_requires_login(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_cart_no_cart(self):
        cart = Cart.objects.filter(user=self.user).delete()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)


@pytest.mark.django_db
class CartViewTest(TestCase):
    def setUp(self):
        self.user = USER_MODEL.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            title="iPhone 16",
            slug="iphone-16",
            category=self.category,
            price=Decimal('999.99'),
            description="Latest iPhone model"
        )

        self.url = reverse('cart:my_cart')

    def test_get_cart_success_no_cart(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_cart_success(self):
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_cart_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


# API TESTS

@pytest.mark.django_db
class CartViewSetTest(APITestCase):
    def setUp(self):
        self.user = USER_MODEL.objects.create_user(username="testuser", password="password")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            title="iPhone 16",
            slug="iphone-16",
            category=self.category,
            price=Decimal('999.99'),
            description="Latest iPhone model"
        )
        self.product_2 = Product.objects.create(
            title="iPhone 15",
            slug="iphone-15",
            category=self.category,
            price=Decimal('899.99'),
            description="15th iPhone model"
        )
        self.url_list = reverse('cart:cart-list')
        self.url_add_item = '/cart/api/cart/add_to_cart/'
        self.url_delete_cart = '/cart/api/cart/delete_cart/'

    def test_get_cart_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 401)

    def test_cart_list(self):
        self.cart = Cart.objects.create(user=self.user)

        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_cart(self):
        response = self.client.post(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cart_items'], [])
        self.assertEqual(response.data['total_price'], 0)
        self.assertEqual(response.data['user'], self.user.username)

    def test_add_item_to_empty_cart(self):
        response = self.client.post(self.url_add_item, data={'product_id': 1, 'quantity': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)

        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.total_price(), Decimal('1999.98'))
        self.assertEqual(cart_item.product.title, 'iPhone 16')

    def test_add_item_to_existing_item_in_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart_item_previous = CartItem.objects.create(cart=cart, product=self.product, quantity=1)

        response = self.client.post(self.url_add_item, data={'product_id': self.product.id, 'quantity': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)

        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(cart.cart_items.count(), 1)

    def test_add_item_to_existing_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)

        response = self.client.post(self.url_add_item, data={'product_id': self.product_2.id, 'quantity': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_cart_item = CartItem.objects.get(cart=cart, product=self.product_2)
        total_count = cart_item.quantity + new_cart_item.quantity
        self.assertEqual(cart_item.quantity, 1)
        self.assertEqual(new_cart_item.quantity, 2)
        self.assertEqual(cart.cart_items.count(), 2)
        self.assertEqual(cart.get_total_price(), Decimal('2799.97'))
        self.assertEqual(total_count, 3)

    def test_add_zero_quantity_item(self):
        response = self.client.post(self.url_add_item, data={'product_id': 1, 'quantity': 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_item_from_cart(self):
        self.client.post(self.url_add_item, data={'product_id': self.product.id, 'quantity': 1})
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        url = f'/cart/api/cart/{cart_item.product.id}/remove_item/'
        response = self.client.delete(url)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_delete_cart(self):
        cart = Cart.objects.create(user=self.user)
        response = self.client.delete(self.url_delete_cart)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(user=self.user).exists())

    def test_delete_cart_requires_login(self):
        self.client.logout()
        response = self.client.delete(self.url_delete_cart)
        self.assertEqual(response.status_code, 401)


@pytest.mark.django_db
class AdminCartViewTest(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)

        self.common_user = CustomUser.objects.create_user('user', 'user@example.com', 'password')
        self.common_client = APIClient()
        self.common_client.force_authenticate(user=self.common_user)

        self.category = Category.objects.create(name="Phones", slug="phones")
        self.product = Product.objects.create(
            title="iPhone 16",
            slug="iphone-16",
            category=self.category,
            price=999.99,
            description="Latest iPhone model"
        )

        self.common_user_cart = Cart.objects.create(user=self.common_user)
        self.admin_user_cart = Cart.objects.create(user=self.admin_user)

        self.common_user_cart_item = CartItem.objects.create(cart=self.common_user_cart, product=self.product,
                                                             quantity=1)
        self.admin_user_cart_item = CartItem.objects.create(cart=self.admin_user_cart, product=self.product, quantity=2)

        self.url = reverse('cart:admin-list')
        self.delete_url = f'/cart/api/admin/{self.common_user.id}/'

    def test_get_all_carts(self):
        response = self.admin_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn(self.common_user_cart, [cart['id'] for cart in response.data])
        self.assertIn(self.admin_user_cart.id, [cart['id'] for cart in response.data])

    def test_common_user_does_not_have_permission(self):
        # Test that a common user cannot retrieve all carts
        response_get = self.common_client.get(self.url)
        self.assertEqual(response_get.status_code, status.HTTP_403_FORBIDDEN)

        # Test that a common user cannot delete someone else's cart
        response_delete = self.common_client.delete(self.delete_url)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_other_user_cart(self):
        response = self.admin_client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(user=self.common_user).exists())
