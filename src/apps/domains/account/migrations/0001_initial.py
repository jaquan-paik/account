# Generated by Django 2.0.2 on 2018-03-28 17:16

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('idx', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='u_idx')),
                ('id', models.CharField(editable=False, max_length=16, unique=True, verbose_name='u_id')),
            ],
            options={
                'verbose_name': '사용자 계정',
                'verbose_name_plural': '사용자 계정 리스트',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='OAuth2User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='이름')),
            ],
            options={
                'verbose_name': 'oauth2 사용자 계정',
                'verbose_name_plural': 'oauth2 사용자 계정 리스트',
                'db_table': 'oauth2_user',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('admin_id', models.CharField(max_length=128, unique=True, verbose_name='어드민 ID')),
            ],
            options={
                'verbose_name': '관리자 계정',
                'verbose_name_plural': '관리자 계정 리스트',
                'db_table': 'staff',
            },
        ),
    ]
