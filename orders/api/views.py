from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from mixins.pagination import CustomPagination
from orders.api.serializers import OrderListSerializer, OrderDetailsSerializer, CreateOrderSerializer
from orders.filters import OrderFilter
from orders.models import Order, OrderItem


class OrderViewSet(ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = OrderFilter
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderDetailsSerializer
        if self.action == "create":
            return CreateOrderSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return (
            Order.objects.select_related("customer__user").prefetch_related(
                Prefetch("items", queryset=OrderItem.objects.select_related("product").order_by("id"))).order_by("id")
        )

    def get(self, request, **kwargs):
        if hasattr(kwargs, "pk"):
            product = get_object_or_404(Order, pk=kwargs["pk"])
            serializer = self.get_serializer(product)
            return Response({"result": serializer.data, "message": "Loaded successfully", "status": True}, status=200)

        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        return Response({"result": serializer.data, "message": "Loaded successfully", "status": True}, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {"result": OrderDetailsSerializer(order).data, "message": "created successfully", "status": True},
                status=201)
        return Response({"message": "Something went wrong!", "errors": serializer.errors}, 400)
