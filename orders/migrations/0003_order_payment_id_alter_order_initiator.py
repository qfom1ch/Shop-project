# Generated by Django 4.1.7 on 2023-04-16 11:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_order_initiator_alter_order_address_alter_order_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Идентификатор платежа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Инициатор'),
        ),
    ]
