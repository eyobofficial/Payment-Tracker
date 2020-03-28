# Generated by Django 2.2.11 on 2020-03-27 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0006_auto_20200327_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryorder',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_delivery_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]