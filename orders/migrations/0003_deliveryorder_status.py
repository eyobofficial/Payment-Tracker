# Generated by Django 2.2.11 on 2020-03-26 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200326_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryorder',
            name='status',
            field=models.CharField(choices=[('OPEN', 'open'), ('CLOSED', 'closed')], default='OPEN', max_length=10),
        ),
    ]
