from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    category_id = filters.CharFilter(field_name="category_id", lookup_expr="exact")
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = {}
