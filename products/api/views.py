from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from mixins.pagination import CustomPagination
from products.api.serializers import ProductSerializer
from products.filters import ProductFilter
from products.models import Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ["name"]
    filterset_class = ProductFilter
    ordering_fields = ("price",)
