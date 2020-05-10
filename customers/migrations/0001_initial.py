# Generated by Django 2.2.11 on 2020-05-10 08:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Customer company or office name.', max_length=120)),
                ('region', models.CharField(max_length=120, unique=True)),
                ('code', models.CharField(max_length=4, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Union',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('location', models.CharField(blank=True, max_length=60)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unions', to='customers.Customer')),
            ],
            options={
                'order_with_respect_to': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='customers.Customer')),
            ],
            options={
                'order_with_respect_to': 'customer',
            },
        ),
    ]
