# Generated by Django 2.2.11 on 2020-05-31 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200531_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryorder',
            name='lc_number',
        ),
    ]
