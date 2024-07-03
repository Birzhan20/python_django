from itertools import product
from random import choices
from string import ascii_letters

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission

from django.conf import settings
from .models import Product, Order
from .utils import add_two_numbers


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        # Добавляем разрешение пользователю
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.order = Order.objects.create(delivery_address='123 Test St', promocode='DISCOUNT10', user=self.user)
        self.product = Product.objects.create(name='Test Product', price=100)
        self.order.products.add(self.product)

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_order_details(self):
        url = reverse('shopapp:order_details', args=[self.order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context['order'].pk, self.order.pk)





# class AddTwoNumbersTestCase(TestCase):
#     def test_add_two_numbers(self):
#         result = add_two_numbers(5, 3)
#         self.assertEqual(result, 5)


# class CreateProductViewTestCase(TestCase):
#
#     def setUp(self):
#         # Создание и аутентификация пользователя
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.user.user_permissions.add(Permission.objects.get(codename='add_product'))
#         self.client.login(username='testuser', password='testpassword')
#         self.product_name = ''.join(choices(ascii_letters, k=10))
#         Product.objects.create(name=self.product_name).delete()
#
#     def test_create_product(self):
#         response = self.client.post(
#             reverse("shopapp:product_create"),
#             {
#                 'name': self.product_name,
#                 'price': '123.45',
#                 'description': 'A good table',
#                 'discount': '10'
#
#             }
#         )
#
#         self.assertRedirects(response, reverse("shopapp:products_list"))
#         self.assertTrue(
#             Product.objects.filter(name=self.product_name).exists()
#         )


# class ProductDetailViewTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.product = Product.objects.create(name='Product 1')
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.product.delete()
#
#     def test_get_product_and_check_content(self):
#         response = self.client.get(
#             reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
#         )
#         self.assertContains(response, self.product.name)


# class ProductListViewTest(TestCase):
#     fixtures = [
#         'products-fixtures.json',
#     ]
#
#     def test_products(self):
#         response = self.client.get(reverse('shopapp:products_list'))
#         self.assertQuerysetEqual(
#             qs=Product.objects.filter(archived=False).all(),
#             values=(p.pk for p in response.context['products']),
#             transform=lambda p: p.pk,
#         )
#         self.assertTemplateUsed(response, 'shopapp/products-list.html')

#


# class ProductExportViewTestCase(TestCase):
#     fixtures = {
#         'products-fixtures.json',
#     }
#
#     def test_get_products_view(self):
#         response = self.client.get(reverse('shopapp:products-export'))
#         self.assertEqual(response.status_code, 200)
#         products = Product.objects.order_by("pk").all()
#         expected_data = [
#             {
#                 'pk': product.pk,
#                 'name': product.name,
#                 'price': str(product.price),
#                 'archived': product.archived,
#             }
#             for product in products
#         ]
#
#         products_data = response.json()
#         self.assertEqual(
#             products_data['products'],
#             expected_data
#         )




