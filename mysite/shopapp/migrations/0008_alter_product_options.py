# Generated by Django 5.0.4 on 2024-06-27 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_rename_discription_product_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price']},
        ),
    ]
