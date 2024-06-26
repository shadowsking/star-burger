# Generated by Django 3.2.15 on 2024-03-17 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, verbose_name='комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Принят', 'Принят'), ('Готовится', 'Готовится'), ('Доставка', 'Доставка'), ('Доставлен', 'Доставлен'), ('Отменен', 'Отменен')], db_index=True, default='Принят', max_length=50, verbose_name='статус заказа'),
        ),
    ]
