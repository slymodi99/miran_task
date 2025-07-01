from model_bakery import baker
from django.test import TestCase


class TestProductsViewSet(TestCase):
    def setUp(self):
        self.url = '/api/products/'
        self.category = baker.make('products.Category', name="beverages")
        self.category2 = baker.make('products.Category', name="food")
        baker.make('products.Product', name="pepsi", price=50.50, inventory_count=100, category=self.category)
        baker.make('products.Product', name="v-cola", price=100.70, inventory_count=115, category=self.category)
        baker.make('products.Product', name="chips", price=15.50, inventory_count=10, category=self.category2)

    def test_get_products(self):
        response = self.client.get(self.url)
        result = response.json()["result"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "pepsi")
        self.assertEqual(result[1]["name"], "v-cola")
        self.assertEqual(result[0]["price"], "50.50")
        self.assertEqual(result[1]["price"], "100.70")
        self.assertEqual(result[0]["inventory_count"], 100)
        self.assertEqual(result[1]["inventory_count"], 115)
        self.assertEqual(result[0]["category"]["name"], "beverages")
        self.assertEqual(result[1]["category"]["name"], "beverages")

    def test_search_products_by_name(self):
        response = self.client.get(self.url + "?search=pepsi")
        result = response.json()["result"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "pepsi")
        self.assertEqual(result[0]["price"], "50.50")

    def test_filter_products_by_category_id(self):
        response = self.client.get(self.url + "?category_id=" + str(self.category2.id))
        result = response.json()["result"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "chips")
        self.assertEqual(result[0]["price"], "15.50")

    def test_filter_products_by_category_name(self):
        response = self.client.get(self.url + "?category_name=" + self.category2.name)
        result = response.json()["result"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "chips")
        self.assertEqual(result[0]["price"], "15.50")
