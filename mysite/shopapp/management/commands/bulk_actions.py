from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        result = Product.objects.filter(
            name__contains='Macbook',
        ).update(discount=10)
        print(result) # 1 командой sql выполнить множество обновление записей пачками

        # info = [
        #     ('Macbook Air', 899),
        #     ('Macbook Pro 14', 1299),
        #     ('Macbook Pro 16', 2499),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        # result = Product.objects.bulk_create(products) # 1 командой sql выполнить множество создание записей пачками
        #
        # for obj in result:
        #     print(obj)

        self.stdout.write("Done")
