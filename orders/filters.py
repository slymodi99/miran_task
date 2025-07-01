from django_filters import rest_framework as filters
from .models import Order


class OrderFilter(filters.FilterSet):
    customer_name = filters.CharFilter(field_name='customer__user__username', lookup_expr='icontains')
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    created_at_from = filters.DateFilter(field_name='created_at__date', lookup_expr='gte')
    created_at_to = filters.DateFilter(field_name='created_at__date', lookup_expr='lte')

    class Meta:
        model = Order
        fields = {}
