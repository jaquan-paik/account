# Generated by Django 2.1.7 on 2019-04-08 12:24

import apps.domains.oauth2.models
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_app', '0004_auto_20190320_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='authorization_grant_type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('authorization-code', 'Authorization code'), ('password', 'Resource owner password-based'), ('client_credentials', 'Client Credentials')], default='authorization-code', help_text='Authorization code와 Password 만 지원한다.', max_length=128, verbose_name='Grant 종류'),
        ),
        migrations.AlterField(
            model_name='refreshtoken',
            name='expires',
            field=models.DateTimeField(default=apps.domains.oauth2.models._get_refresh_token_expires, editable=False, verbose_name='만료일'),
        ),
        migrations.AlterField(
            model_name='refreshtoken',
            name='token',
            field=models.CharField(default=apps.domains.oauth2.models._create_random_refresh_token, max_length=30, unique=True),
        ),
    ]
