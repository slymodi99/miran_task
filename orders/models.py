from django.db import models

from mixins.models import Timestamps
from products.models import Product
from users.models import Customer


class Order(Timestamps):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.PROTECT)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['customer_id', 'status'], name='order_customer_status_idx'),
        ]

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)