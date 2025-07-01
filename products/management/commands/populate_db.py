
from django.core.management.base import BaseCommand
from users.models import User, Customer
from products.models import Category, Product
from orders.models import Order, OrderItem
from django.utils import timezone
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("loading...")

        # add categories
        category_names = ['Electronics', 'Clothing', 'Books', 'Toys', 'Furniture']
        categories = []
        for name in category_names:
            cat = Category.objects.create(name=name)
            categories.append(cat)

        # add products
        products = []
        for _ in range(100):
            name = fake.unique.word().capitalize()
            price = round(random.uniform(5, 1500), 2)
            category = random.choice(categories)
            inventory = random.randint(10, 200)
            product = Product.objects.create(
                name=name,
                price=price,
                category=category,
                inventory_count=inventory
            )
            products.append(product)

        # add customers
        customers = []
        for i in range(100):
            phone = f"010{fake.unique.random_number(digits=8)}"
            user_name = fake.unique.user_name()
            user = User.objects.create_user(
                user_phone=phone,
                username=user_name,
                password="password123",
                email=fake.unique.email()
            )
            customer = Customer.objects.create(
                user=user,
                address_title=fake.city(),
                address_details=fake.address()
            )
            customers.append(customer)

        # add orders
        statuses = ['pending', 'shipped', 'cancelled']
        for _ in range(100):
            customer = random.choice(customers)
            grand_total = round(random.uniform(200, 15000), 2)
            order = Order.objects.create(
                customer=customer,
                status=random.choice(statuses),
                created_at=timezone.now(),
                grand_total=grand_total
            )

            order_products = random.sample(products, k=random.randint(1, 5))
            for product in order_products:
                quantity = random.randint(1, 5)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price
                )

        print("Done")
