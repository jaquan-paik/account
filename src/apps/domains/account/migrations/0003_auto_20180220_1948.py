# Generated by Django 2.0.2 on 2018-02-20 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0002_oauth2user'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='oauth2user',
            table='oauth2_user',
        ),
    ]