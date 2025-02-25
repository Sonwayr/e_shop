import pytest
from django.test import TestCase
from e_shop.models import Category, Product


@pytest.mark.django_db
class CategoryModelTest(TestCase):

    def setUp(self):
        """
        Create a parent and child category for use in unit tests.
        """

        self.parent_category = Category.objects.create(name="Electronics", slug="electronics")
        self.child_category = Category.objects.create(name="Laptops", parent=self.parent_category, slug="laptops")

    def test_category_str_child(self):
        self.assertEqual(str(self.child_category), "Electronics -> Laptops")

    def test_category_str_parent(self):
        self.assertEqual(str(self.parent_category), "Electronics")

    def test_category_slug(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.slug, "test-category")

    def test_category_parent_url(self):
        self.assertEqual(self.parent_category.get_absolute_url(), "/electronics/")

    def test_category_child_url(self):
        self.assertEqual(self.child_category.get_absolute_url(), "/laptops/")


@pytest.mark.django_db
class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Phones", slug="phones")
        self.product = Product.objects.create(
            category=self.category,
            title="iPhone 16",
            brand="Apple",
            description="Latest iPhone model",
            price=999.99,
            slug="iphone-16"
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "iPhone 16")

    def test_product_slug(self):
        self.assertEqual(self.product.slug, "iphone-16")

    def test_product_price(self):
        self.assertEqual(self.product.price, 999.99)

    def test_product_url(self):
        self.assertEqual(self.product.get_absolute_url(), "/product/iphone-16/")
