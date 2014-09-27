# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nwk', '0004_auto_20140920_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('website', models.URLField(blank=True)),
                ('picture', models.URLField(blank=True)),
                ('point', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('badge', models.PositiveIntegerField()),
                ('device_token', models.CharField(max_length=250)),
                ('device_type', models.CharField(max_length=6)),
                ('app_name', models.CharField(max_length=20)),
                ('app_version', models.PositiveIntegerField()),
                ('customer', models.ForeignKey(to='nwk.Consumer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Retail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('shop_name', models.CharField(max_length=30)),
                ('logo_url', models.URLField(blank=True)),
                ('location_level', models.PositiveSmallIntegerField()),
                ('location_unit', models.PositiveSmallIntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='consumer',
            name='favorite_shops',
            field=models.ManyToManyField(to='nwk.Retail'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consumer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='promotion',
            name='grabbed_by',
            field=models.ManyToManyField(to='nwk.Consumer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 27, 14, 23, 17, 115790)),
        ),
    ]
