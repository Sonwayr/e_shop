from django.contrib import admin
from .models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug', 'created_at', 'updated_at']
    ordering = ('name', 'created_at', 'updated_at')

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'category', 'title', 'brand', 'description', 'slug',
        'price', 'image_tag', 'available', 'created_at', 'updated_at'
    ]
    ordering = ('title', 'created_at', 'updated_at', 'price', 'available')
    list_display_links = ['title', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}