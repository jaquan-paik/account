# Generated by Django 2.1.7 on 2019-03-20 12:50

import apps.domains.oauth2.models
from django.db import migrations, models
import lib.django.db.mysql


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_app', '0003_auto_20180504_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='redirect_uris',
        ),
        migrations.AddField(
            model_name='application',
            name='_redirect_uris',
            field=models.TextField(db_column='redirect_uris', default=' '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='authorization_grant_type',
            field=models.CharField(choices=[('authorization-code', 'Authorization code'), ('password', 'Resource owner password-based')], default='authorization-code', help_text='Authorization code와 Password 만 지원한다.', max_length=32, verbose_name='Grant 종류'),
        ),
        migrations.AlterField(
            model_name='application',
            name='is_in_house',
            field=lib.django.db.mysql.TinyBooleanField(default=False, verbose_name='내부 서비스 여부'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='code',
            field=models.CharField(default=apps.domains.oauth2.models._create_random_code, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='expires',
            field=models.DateTimeField(default=apps.domains.oauth2.models._get_grant_expires),
        ),
    ]