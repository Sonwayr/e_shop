from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'e_shop'

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('product/<slug:slug>/', views.DetailProduct.as_view(), name='product'),
    path('<slug:category_slug>/', views.MainPage.as_view(), name='products_by_category'),

    path('api/', include(router.urls)),

]
