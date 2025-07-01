from decimal import Decimal

from django.db import transaction
from django.db.models import F, When, Case
from rest_framework import serializers

from orders.models import OrderItem, Order
from products.models import Product


class OrderCreationError(serializers.ValidationError):
    pass


class OrderCreationService:
    def __init__(self, customer_id, items):
        self.customer_id = customer_id
        self.items = items or []
        self.product_map = {}

    def _validate_products_and_inventory(self):
        product_ids = [item['product_id'] for item in self.items]

        products = Product.objects.select_for_update().filter(
            id__in=product_ids,
        )

        self.product_map = {p.id: p for p in products}

        errors = []
        for item in self.items:
            product = self.product_map.get(item['product_id'])
            if not product:
                errors.append(f"Product ID {item['product_id']} does not exist.")
                continue

            if item['quantity'] > product.inventory_count:
                errors.append(
                    f"Inventory limit exceeded for '{product.id}'. "
                    f"Maximum available: {product.inventory_count} units"
                )

        if errors:
            raise OrderCreationError({"inventory_errors": errors})

    def validate(self):
        self._validate_products_and_inventory()

    def _calculate_totals(self):
        order_items_data = []
        grand_total = Decimal('0.00')

        for item in self.items:
            product = self.product_map[item['product_id']]
            quantity = item['quantity']
            unit_price = product.price
            total_price = unit_price * quantity

            order_items_data.append({
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price,
            })
            grand_total += total_price

        return order_items_data, grand_total

    @staticmethod
    def _update_inventory(order_items_data):
        product_quantities = {
            item['product'].id: item['quantity']
            for item in order_items_data
        }

        when_statements = [
            When(id=product_id, then=F('inventory_count') - quantity)
            for product_id, quantity in product_quantities.items()
        ]

        Product.objects.filter(id__in=product_quantities.keys()).update(
            inventory_count=Case(*when_statements)
        )

    def _create_order_and_items(self, order_items_data, grand_total):
        order = Order.objects.create(
            customer_id=self.customer_id,
            status='pending',
            grand_total=grand_total
        )

        order_items = []
        for item_data in order_items_data:
            order_items.append(OrderItem(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price']
            ))

        OrderItem.objects.bulk_create(order_items)
        return order

    @transaction.atomic
    def create_order(self):
        try:
            self.validate()
            order_items_data, grand_total = self._calculate_totals()

            self._update_inventory(order_items_data)

            order = self._create_order_and_items(order_items_data, grand_total)
            return order
        except Exception as e:
            raise OrderCreationError(f"Order creation failed: {str(e)}")
