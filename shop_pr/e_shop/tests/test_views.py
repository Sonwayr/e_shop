from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from e_shop.models import Category, Product
from users.models import CustomUser
from rest_framework.test import APIClient
from decimal import Decimal
import pytest


@pytest.mark.django_db
class MainPageViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product_1 = Product.objects.create(
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
            price=Decimal('799.99'),
            description="15th iPhone model"
        )

    def test_main_page_status_code(self):
        response = self.client.get(reverse('e_shop:main_page'))
        self.assertEqual(response.status_code, 200)

    def test_main_page_with_category(self):
        response = self.client.get(reverse('e_shop:products_by_category', kwargs={'category_slug': 'electronics'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product_1.title)

    def test_main_page_sort_by_price_asc(self):
        response = self.client.get(reverse('e_shop:main_page') + '?sort=price_asc')
        self.assertEqual(response.status_code, 200)

        products = response.context['products']
        self.assertEqual(products[0].price, self.product_2.price)

    def test_main_page_sort_by_title_desc(self):
        response = self.client.get(reverse('e_shop:main_page') + '?sort=title_desc')
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products[0].title, self.product_1.title)


@pytest.mark.django_db
class DetailProductViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Phones", slug="phones")
        self.product = Product.objects.create(
            title="iPhone 16",
            slug="iphone-16",
            category=self.category,
            price=999.99,
            description="Latest iPhone model"
        )

    def test_detail_product_status_code(self):
        response = self.client.get(reverse('e_shop:product', kwargs={'slug': 'iphone-16'}))
        self.assertEqual(response.status_code, 200)

    def test_detail_product_contains_product_data(self):
        response = self.client.get(reverse('e_shop:product', kwargs={'slug': 'iphone-16'}))
        self.assertContains(response, self.product.title)


# API


@pytest.mark.django_db
class ProductViewSetTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Phones", slug="phones")
        self.product = Product.objects.create(
            title="iPhone 16",
            slug="iphone-16",
            category=self.category,
            price=999.99,
            description="Latest iPhone model"
        )
        self.url = reverse('e_shop:product-list')

    def test_product_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        data = {
            'category': self.category.id,
            'title': 'iPhone 17',
            'brand': 'Apple',
            'description': 'Newest iPhone model',
            'slug': 'iphone-17',
            'price': Decimal(1099.99)
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'iPhone 17')

    def test_update_product(self):
        data = {
            'price': 899.99
        }
        response = self.client.patch(reverse('e_shop:product-detail', kwargs={'pk': self.product.id}), data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '899.99')

    def test_delete_product(self):
        response = self.client.delete(reverse('e_shop:product-detail', kwargs={'pk': self.product.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


@pytest.mark.django_db
class CategoryViewSetTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Phones", slug="phones")
        self.url = reverse('e_shop:category-list')

    def test_category_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        data = {
            'name': 'Tablets',
            'slug': 'tablets',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Tablets')

    def test_update_category(self):
        data = {
            'name': 'Smartphones'
        }
        response = self.client.patch(reverse('e_shop:category-detail', kwargs={'pk': self.category.id}), data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Smartphones')

    def test_delete_category(self):
        response = self.client.delete(reverse('e_shop:category-detail', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
