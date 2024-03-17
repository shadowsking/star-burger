# Generated by Django 3.2.15 on 2024-03-17 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_auto_20240317_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('Наличные', 'Наличные'), ('Электронные', 'Электронные')], db_index=True, default='Электронные', max_length=50, verbose_name='способ оплаты'),
        ),
    ]
