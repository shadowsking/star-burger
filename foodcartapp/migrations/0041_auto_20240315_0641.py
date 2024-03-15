# Generated by Django 3.2.15 on 2024-03-15 03:41

from django.db import migrations


def migrate_price_from_product(apps, schema_editor):
    OrderedProduct = apps.get_model('foodcartapp', 'OrderedProduct')
    for ordered_product in OrderedProduct.objects.all():
        ordered_product.price = ordered_product.product.price
        ordered_product.save()


class Migration(migrations.Migration):
    dependencies = [
        ('foodcartapp', '0040_orderedproduct_price'),
    ]

    operations = [
        migrations.RunPython(migrate_price_from_product),
    ]
