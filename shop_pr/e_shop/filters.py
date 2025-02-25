import django_filters
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .utils import get_category_ids


class ProductFilter(django_filters.FilterSet):
    category_slug = django_filters.CharFilter(field_name='category__slug', method='category_filter')
    brand_slug = django_filters.CharFilter(field_name='brand_slug', lookup_expr='iexact')
    available = django_filters.BooleanFilter(field_name='available')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category_slug', 'available', 'min_price', 'max_price', 'brand_slug']

    def category_filter(self, queryset, name, value):
        category_ids = get_category_ids(value)
        return queryset.filter(category_id__in=category_ids)


class CategoryFilter(django_filters.FilterSet):
    slug = django_filters.CharFilter(field_name='slug', method='category_filter')

    class Meta:
        model = Category
        fields = ['slug']

    def category_filter(self, queryset, name, value):
        category_ids = get_category_ids(value)
        return queryset.filter(id__in=category_ids)
