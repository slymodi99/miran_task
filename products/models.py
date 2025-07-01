from django.db import models

from mixins.models import Timestamps


class Category(Timestamps):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(Timestamps):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    inventory_count = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['name', 'price'], name='product_name_price_idx'),
        ]

    def __str__(self):
        return self.name
