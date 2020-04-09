# Generated by Django 2.2.11 on 2020-04-04 20:35

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
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
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, verbose_name='company name')),
                ('city', models.CharField(max_length=60)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('code', models.CharField(max_length=10)),
                ('type', models.CharField(choices=[('WEIGHT', 'Weight/Mass'), ('VOLUME', 'Volume'), ('LENGTH', 'Length/Distance'), ('COUNTER', 'Counter')], max_length=10)),
            ],
            options={
                'verbose_name': 'Measurement Unit',
                'verbose_name_plural': 'Measurement Units',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shared.ProductCategory')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shared.Unit')),
            ],
            options={
                'ordering': ('name',),
                'default_related_name': 'products',
            },
        ),
        migrations.CreateModel(
            name='Union',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unions', to='shared.Customer')),
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
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='shared.Customer')),
            ],
            options={
                'order_with_respect_to': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('quantity', models.DecimalField(decimal_places=2, help_text='Quantity in the selected product unit.', max_digits=10)),
                ('rate', models.DecimalField(decimal_places=2, help_text='Price is in USD.', max_digits=10)),
                ('batch_round', models.PositiveSmallIntegerField(default=1, help_text='Batch round for the year.')),
                ('year', models.PositiveIntegerField(choices=[(2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], default=2020)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batches', to='shared.Product')),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batches', to='shared.Supplier')),
            ],
            options={
                'verbose_name': 'Purchasing Batch',
                'verbose_name_plural': 'Purchasing Batches',
                'default_related_name': 'batches',
                'unique_together': {('name', 'product', 'batch_round', 'year')},
            },
        ),
    ]
