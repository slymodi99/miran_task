from django.test import TestCase
from model_bakery import baker

from products.models import Product
from rest_framework.test import APIClient


def place_order_concurrently(url, data):
    client = APIClient()
    response = client.post(url, data=data, content_type="application/json")
    return response.status_code


class TestOrdersViewSet(TestCase):
    def setUp(self):
        self.url = '/api/orders/'
        self.category = baker.make('products.Category', name="beverages")
        self.category2 = baker.make('products.Category', name="food")
        self.user = baker.make('users.User', username="test_user", user_phone="01024541248")
        self.customer = baker.make('users.Customer', user=self.user)
        self.user2 = baker.make('users.User', username="ronaldo", user_phone="01054541248")
        self.customer2 = baker.make('users.Customer', user=self.user2)
        self.p1 = baker.make('products.Product', name="pepsi", price=50.50, inventory_count=100, category=self.category)
        self.p2 = baker.make('products.Product', name="v-cola", price=100.70, inventory_count=115,
                             category=self.category)
        self.p3 = baker.make('products.Product', name="chips", price=15.50, inventory_count=10, category=self.category2)

    def test_create_order_success(self):
        data = {
            "customer_id": self.customer.id,
            "items": [
                {
                    "product_id": self.p1.id,
                    "quantity": 5
                },
                {
                    "product_id": self.p2.id,
                    "quantity": 2
                }
            ]
        }
        response = self.client.post(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["result"]["status"], "pending")
        self.assertEqual(response.json()["result"]["customer_name"], "test_user")
        self.assertEqual(response.json()["result"]["grand_total"], "453.90")

    def test_create_order_with_invalid_customer_id(self):
        data = {
            "customer_id": 1000,
            "items": [
                {
                    "product_id": self.p1.id,
                    "quantity": 5
                },
                {
                    "product_id": self.p2.id,
                    "quantity": 5
                }
            ]
        }
        response = self.client.post(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["errors"],
            {'customer_id': ['Invalid id - customer "1000" does not exist']}
        )

    def test_create_order_with_invalid_item_id(self):
        data = {
            "customer_id": self.customer.id,
            "items": [
                {
                    "product_id": self.p1.id,
                    "quantity": 5
                },
                {
                    "product_id": 100000,
                    "quantity": 10
                }
            ]
        }
        response = self.client.post(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            ["Order creation failed: {'inventory_errors': [ErrorDetail(string='Product ID 100000 does not exist.', code='invalid')]}"]
        )

    def test_create_order_with_invalid_quantity(self):
        data = {
            "customer_id": self.customer.id,
            "items": [
                {
                    "product_id": self.p1.id,
                    "quantity": 5
                },
                {
                    "product_id": self.p2.id,
                    "quantity": 10000
                }
            ]
        }
        response = self.client.post(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_order_validate_that_product_quantity_is_decreased_after_order_creation(self):
        data = {
            "customer_id": self.customer.id,
            "items": [
                {
                    "product_id": self.p1.id,
                    "quantity": 5
                },
                {
                    "product_id": self.p2.id,
                    "quantity": 2
                }
            ]
        }
        response = self.client.post(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["result"]["status"], "pending")
        self.assertEqual(response.json()["result"]["customer_name"], "test_user")
        self.assertEqual(response.json()["result"]["grand_total"], "453.90")
        products = Product.objects.filter(id__in=[self.p1.id, self.p2.id]).order_by("id")
        self.assertEqual(products[0].inventory_count, 95)
        self.assertEqual(products[1].inventory_count, 113)


    def test_list_orders(self):
        baker.make('orders.Order', customer=self.customer, status="pending")
        baker.make('orders.Order', customer=self.customer, status="shipped")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["result"]), 2)
        self.assertEqual(response.json()["result"][0]["status"], "pending")
        self.assertEqual(response.json()["result"][1]["status"], "shipped")
        self.assertEqual(response.json()["result"][0]["customer_name"], "test_user")
        self.assertEqual(response.json()["result"][1]["customer_name"], "test_user")

    def test_list_orders_filtered_by_status(self):
        baker.make('orders.Order', customer=self.customer, status="pending")
        baker.make('orders.Order', customer=self.customer, status="shipped")
        response = self.client.get(self.url + "?status=pending")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["result"]), 1)
        self.assertEqual(response.json()["result"][0]["status"], "pending")

    def test_list_orders_filtered_by_customer_name(self):
        baker.make('orders.Order', customer=self.customer, status="pending")
        baker.make('orders.Order', customer=self.customer2, status="shipped")
        response = self.client.get(self.url + "?customer_name=test_user")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["result"]), 1)
        self.assertEqual(response.json()["result"][0]["status"], "pending")
        self.assertEqual(response.json()["result"][0]["customer_name"], "test_user")

    def test_list_orders_filtered_by_date_range(self):
        baker.make('orders.Order', customer=self.customer, status="pending", created_at="2023-01-01T00:00:00Z")
        baker.make('orders.Order', customer=self.customer, status="shipped", created_at="2023-01-02T00:00:00Z")
        baker.make('orders.Order', customer=self.customer2, status="shipped", created_at="2023-01-03T00:00:00Z")
        response = self.client.get(self.url + "?created_at_from=2023-01-01&created_at_to=2023-01-02")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["result"]), 2)

    def test_get_order_by_id_with_items(self):
        order = baker.make('orders.Order', customer=self.customer, status="pending", grand_total=1400, )
        baker.make('orders.OrderItem', order=order, product=self.p1, quantity=5)
        baker.make('orders.OrderItem', order=order, product=self.p2, quantity=2)
        response = self.client.get(f'{self.url}{str(order.id)}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 2)
        self.assertEqual(response.json()["items"][0]["product_name"], "pepsi")
        self.assertEqual(response.json()["items"][1]["product_name"], "v-cola")
        self.assertEqual(response.json()["items"][0]["quantity"], 5)
        self.assertEqual(response.json()["items"][1]["quantity"], 2)
        self.assertEqual(response.json()["grand_total"], '1400.00')
        self.assertEqual(response.json()["status"], "pending")
        self.assertEqual(response.json()["customer_name"], "test_user")
