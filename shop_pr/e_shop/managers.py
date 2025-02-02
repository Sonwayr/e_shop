from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        """Return only products that are available."""
        return super().get_queryset().filter(available=True)


class ProductNotAvailableManager(models.Manager):
    def get_queryset(self):
        """Return only products that are not available."""
        queryset = super().get_queryset()
        return queryset.filter(available=False)


class ProductAllManager(models.Manager):
    def get_queryset(self):
        """Return all products."""
        return super().get_queryset()
