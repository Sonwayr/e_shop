from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from .managers import ProductManager, ProductNotAvailableManager, ProductAllManager


class Category(models.Model):
    """
    Represents a category in the e-shop_pr.

    Attributes:
        name (str): The name of the category.
        parent (Category): The parent category, if any.
        slug (str): The URL-friendly identifier for the category.
        created_at (datetime): The date and time the category was created.
        updated_at (datetime): The date and time the category was last updated.

    Methods:
        __str__(): Returns a string representation of the category.
    """

    name = models.CharField('Category', max_length=255, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField('URL', max_length=255, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Date of create', auto_now_add=True)
    updated_at = models.DateTimeField('Update date', auto_now=True)

    class Meta:
        unique_together = (['parent', 'slug'])
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        """Returns a string representation of the category."""
        category_names = []
        current_category = self
        while current_category is not None:
            category_names.append(current_category.name)
            current_category = current_category.parent
        return ' -> '.join(reversed(category_names))

    def save(self, *args, **kwargs):
        """Save the category, generating a slug if it doesn't exist."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the URL for the category detail view."""
        return reverse('e_shop:products_by_category', kwargs={'category_slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=255)
    brand = models.CharField('Brand', max_length=255)
    description = models.TextField('Description')
    slug = models.SlugField('URL', max_length=255, unique=True, null=False, editable=True)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2, default=100.00)
    image = models.ImageField('Image', upload_to='products/%Y/%m/%d', null=True, blank=True)
    available = models.BooleanField('Available', default=True)
    created_at = models.DateTimeField('Date of create', auto_now_add=True)
    updated_at = models.DateTimeField('Update date', auto_now=True)

    objects = ProductManager()
    not_available = ProductNotAvailableManager()
    all_products = ProductAllManager()

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" width="100" height="100" /></a>')
        return "No Image"

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('e_shop:product', kwargs={'slug': self.slug})
