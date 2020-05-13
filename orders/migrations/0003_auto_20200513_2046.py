# Generated by Django 2.2.11 on 2020-05-13 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200513_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryorder',
            name='quantity',
            field=models.DecimalField(decimal_places=4, max_digits=10, verbose_name='agreement quantity'),
        ),
        migrations.AlterField(
            model_name='unionallocation',
            name='quantity',
            field=models.DecimalField(decimal_places=4, help_text='Quantity allocated to the union in product unit.', max_digits=10, verbose_name='allocated quantity'),
        ),
        migrations.AlterField(
            model_name='uniondistribution',
            name='over',
            field=models.DecimalField(decimal_places=4, help_text='Over quantity supplied in product unit.', max_digits=10, verbose_name='over supplied quantity'),
        ),
        migrations.AlterField(
            model_name='uniondistribution',
            name='quantity',
            field=models.DecimalField(decimal_places=4, help_text='Quantity received by the union in product unit.', max_digits=10, verbose_name='received quantity'),
        ),
        migrations.AlterField(
            model_name='uniondistribution',
            name='shortage',
            field=models.DecimalField(decimal_places=4, help_text='Quantity deficit after transportation in product unit.', max_digits=10, verbose_name='dispatch shortage'),
        ),
    ]
