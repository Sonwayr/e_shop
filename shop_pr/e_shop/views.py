from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter, CategoryFilter
from .models import Category
from .models import Product
from .serializers import CategorySerializer, ProductSerializer


class MainPage(TemplateView):
    template_name = 'e_shop/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_option = self.request.GET.get('sort')
        cat_slug = kwargs.get('category_slug')

        if cat_slug:
            category = get_object_or_404(Category, slug=cat_slug)
            full_category_name = [category] + list(category.children.all())
            products = Product.objects.filter(category__in=full_category_name)
        else:
            products = Product.objects.all()
            category = None

        if sort_option == 'price_asc':
            products = products.order_by('price')
        elif sort_option == 'price_desc':
            products = products.order_by('-price')
        elif sort_option == 'title_asc':
            products = products.order_by('title')
        elif sort_option == 'title_desc':
            products = products.order_by('-title')
        elif sort_option == 'newest':
            products = products.order_by('-created_at')

        context['products'] = products
        context['category'] = category
        context['categories'] = Category.objects.all()
        return context


class DetailProduct(DetailView):
    model = Product
    template_name = 'e_shop/product.html'
    slug_url_kwarg = 'slug'
    extra_context = {'categories': Category.objects.all()}


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    queryset = Product.all_products.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'title', 'created_at']


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CategoryFilter
    ordering_fields = ['name', 'created_at']
