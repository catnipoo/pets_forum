# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-05-11 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attitude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('attitude', models.SmallIntegerField(choices=[(1, '赞'), (2, '踩')], verbose_name='评价')),
            ],
            options={
                'verbose_name': '文章评价',
                'verbose_name_plural': '文章评价',
                'db_table': 'trends_attitude',
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('channel_name', models.CharField(max_length=32, verbose_name='频道名')),
            ],
            options={
                'verbose_name': '频道',
                'verbose_name_plural': '频道',
                'db_table': 'trends_channel',
            },
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('conent', models.TextField(max_length=9999, verbose_name='评论')),
            ],
            options={
                'verbose_name': '文章评论',
                'verbose_name_plural': '文章评论',
                'db_table': 'trends_commit',
            },
        ),
        migrations.CreateModel(
            name='ImgInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('img', models.ImageField(upload_to='trends_image', verbose_name='图片')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片',
                'db_table': 'trends_image',
            },
        ),
        migrations.CreateModel(
            name='Trends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=1000, verbose_name='标题')),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
                ('likes_count', models.IntegerField(default=0, verbose_name='点赞数')),
                ('content', models.TextField(default='如题', verbose_name='正文')),
                ('channel_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trends.Channel', verbose_name='频道')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'trends_info',
            },
        ),
    ]
