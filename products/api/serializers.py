from rest_framework import serializers

from mixins.serializers import ReadOnlySerializer


class CategorySerializer(ReadOnlySerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class ProductSerializer(ReadOnlySerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    inventory_count = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
