from rest_framework import serializers

from mixins.date_formats import Formats
from mixins.serializers import ReadOnlySerializer
from orders.services.create_order_service import OrderCreationService
from users.models import Customer


class OrderListSerializer(ReadOnlySerializer):
    id = serializers.IntegerField(read_only=True)
    customer_name = serializers.CharField(read_only=True, source="customer.user.username")
    grand_total = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format=Formats.datetime)


class OrderItemsSerializer(ReadOnlySerializer):
    id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(read_only=True, source="product.name")
    quantity = serializers.IntegerField(read_only=True)
    unit_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)


class OrderDetailsSerializer(ReadOnlySerializer):
    id = serializers.IntegerField(read_only=True)
    customer_name = serializers.CharField(read_only=True, source="customer.user.username")
    grand_total = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format=Formats.datetime)
    items = OrderItemsSerializer(many=True, read_only=True)


class CreateOrderSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Customer.objects.all(),
        error_messages={
            "does_not_exist": 'Invalid id - customer "{pk_value}" does not exist'
        }
    )
    items = serializers.ListField(
        required=True,
        child=serializers.DictField()
    )

    def create(self, validated_data):
        customer = validated_data["customer_id"]
        items = validated_data["items"]
        return OrderCreationService(
            customer_id=customer.id,
            items=items
        ).create_order()
