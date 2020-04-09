# Generated by Django 2.2.11 on 2020-04-06 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200405_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distribution',
            name='shortage',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Quantity deficit after transportation in product unit.', max_digits=10, verbose_name='dispatch shortage'),
        ),
    ]