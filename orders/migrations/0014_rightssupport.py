# Generated by Django 2.1.5 on 2020-07-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20200629_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='RightsSupport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('see_monitor', 'STAFF rights to monitor'), ('client', 'Client rights')),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]
