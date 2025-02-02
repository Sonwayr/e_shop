from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, verbose_name='Phone number')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Address(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=100, verbose_name='Street')
    house_number = models.CharField(max_length=10, verbose_name='House number')
    city = models.CharField(max_length=50, verbose_name='City')
    country = models.CharField(max_length=50, verbose_name='Country')
    zip_code = models.CharField(max_length=10, verbose_name='Zip code')

    def __str__(self):
        return f'{self.street}, {self.house_number}, {self.city}, {self.country}'


