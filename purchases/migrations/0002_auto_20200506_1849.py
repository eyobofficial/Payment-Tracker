# Generated by Django 2.2.11 on 2020-05-06 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='year',
            field=models.PositiveIntegerField(choices=[('2018/2019', 2018), ('2019/2020', 2019), ('2020/2021', 2020), ('2021/2022', 2021), ('2022/2023', 2022), ('2023/2024', 2023)], default=2020),
        ),
    ]
