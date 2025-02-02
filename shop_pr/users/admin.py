from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'phone_number', 'addresses'
    ]
    ordering = ['is_staff', 'username', 'first_name', 'last_name']
