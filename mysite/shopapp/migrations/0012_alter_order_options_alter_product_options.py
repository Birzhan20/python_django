# Generated by Django 5.0.4 on 2024-07-13 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0011_productimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]
