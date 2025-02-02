from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cart', views.CartViewSet, basename='cart')
router.register(r'admin', views.AdminCartViewSet, basename='admin')

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/<int:product_id>/<int:quantity>', views.add_to_cart, name='add_to_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    path('my_cart/', views.CartView.as_view(), name='my_cart'),

    path('api/', include(router.urls)),
]
