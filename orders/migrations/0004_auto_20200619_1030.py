# Generated by Django 2.1.5 on 2020-06-19 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20200617_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='pasta',
            name='type',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='plate',
            name='type',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='salad',
            name='type',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='sub_addon',
            name='type',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='topping',
            name='type',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='pizzaprice',
            unique_together={('pizza_type', 'pizza_size', 'n_tops')},
        ),
    ]