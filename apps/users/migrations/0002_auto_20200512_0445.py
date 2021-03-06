# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-05-12 04:45
from __future__ import unicode_literals

from django.db import migrations, models
import system.storage


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_active',
            field=models.BooleanField(default=False, verbose_name='邮箱验证状态'),
        ),
        migrations.AlterField(
            model_name='user',
            name='default_image',
            field=models.ImageField(null=True, storage=system.storage.ImageStorage(), upload_to='user_image/%Y/%m/%d', verbose_name='头像'),
        ),
    ]
