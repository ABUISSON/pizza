# Generated by Django 2.1.5 on 2020-06-22 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200619_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sub_main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('size', models.CharField(choices=[('S', 'Small'), ('L', 'Large')], max_length=1)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.AlterField(
            model_name='pizza',
            name='toppings',
            field=models.ManyToManyField(blank=True, to='orders.Topping'),
        ),
        migrations.AlterField(
            model_name='sub',
            name='addons',
            field=models.ManyToManyField(blank=True, to='orders.Sub_addon'),
        ),
    ]
