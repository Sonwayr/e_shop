from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Address
from .serializers import UserSerializer


class CustomUserCreationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('e_shop:main_page')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('e_shop:main_page')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def get_initial(self):
        user = self.request.user
        try:
            address = user.addresses
        except Address.DoesNotExist:
            address = None
        else:

            initial = super().get_initial()

            if address:
                initial['street'] = address.street
                initial['house_number'] = address.house_number
                initial['city'] = address.city
                initial['country'] = address.country
                initial['zip_code'] = address.zip_code

            return initial


class UserViewSet(ModelViewSet):
    """
    Viewset for managing user data.

    This viewset provides endpoints for retrieving and creating user data.
    It is designed to be used for managing the current user's data.
    """

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Return a queryset of users filtered by the current user's PK if authenticated.

        Raises:
            NotFound: If the user is not authenticated.
        """
        user = self.request.user
        if user.is_authenticated:
            return CustomUser.objects.filter(pk=user.pk)
        raise NotFound('User not found')

    def create(self, request, *args, **kwargs):
        """
        Create a new user.

        This method is only accessible when the user is not authenticated.

        Raises:
            PermissionDenied: If the user is already authenticated.
        """
        if request.user.is_authenticated:
            raise PermissionDenied('Authenticated users cannot create users.')
        return super().create(request, *args, **kwargs)


class AdminUserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """
        Return a queryset of all users.

        Returns:
            QuerySet[CustomUser]: A queryset of all users.
        """
        return CustomUser.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
        Delete a user.

        This method is only accessible by admin users.

        Returns:
            Response: A response object with the deleted user's data.

        Raises:
            NotFound: If the user does not exist.
            PermissionDenied: If the user is not an admin.
        """
        return super().destroy(request, *args, **kwargs)
