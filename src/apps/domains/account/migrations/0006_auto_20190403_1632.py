# Generated by Django 2.1.7 on 2019-04-03 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account_app', '0005_auto_20190403_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ip',
            field=models.GenericIPAddressField(null=True, verbose_name='ip'),
        ),
    ]
