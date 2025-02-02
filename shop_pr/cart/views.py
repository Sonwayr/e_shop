from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from e_shop.models import Product
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .serializers import CartSerializer
from .models import Cart, CartItem


# Create your views here.
@login_required
def add_to_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity += quantity - 1
    cart_item.save()

    return redirect('e_shop:main_page')


@login_required
def delete_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.delete()
    return redirect('e_shop:main_page')


class CartView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = self.object.cart_items.all()
        return context

    def get_object(self, queryset=None):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart = Cart.objects.filter(user=user)
        return cart

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='add_to_cart')
    def add_item(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if quantity <= 0:
            return Response({'error': 'Quantity must be greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity += quantity - 1
        cart_item.save()

        return Response({'message': 'Item added to cart successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='delete_cart')
    def delete_cart(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.delete()
            return Response({'message': 'Cart deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'], url_path='remove_item')
    def remove_item(self, request, pk=None):
        try:
            cart = Cart.objects.get(user=request.user)
            product = Product.objects.get(id=pk)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({'message': 'Item removed from cart successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not in cart.'}, status=status.HTTP_404_NOT_FOUND)


class AdminCartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Cart.objects.all()

    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            cart = Cart.objects.get(user__id=user_id)
            cart.delete()
            return Response({'message': 'Cart deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)