# Generated by Django 2.2.11 on 2020-04-12 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_deliveryorder_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryorder',
            name='lc_number',
            field=models.CharField(max_length=30, verbose_name='letter of credit number'),
        ),
    ]