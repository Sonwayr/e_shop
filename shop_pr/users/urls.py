from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')
router.register(r'admin', views.AdminUserViewSet, basename='admin')

app_name = 'users'

urlpatterns = [
    path('register/', views.CustomUserCreationView.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my_profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.ProfileUpdateView.as_view(), name='edit_profile'),

    path('api/', include(router.urls)),

]
