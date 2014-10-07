# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0008_auto_20140927_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('badge', models.PositiveIntegerField()),
                ('device_token', models.CharField(max_length=250)),
                ('device_type', models.CharField(max_length=6)),
                ('timezone', models.CharField(max_length=20, default='Asia/Singapore')),
                ('app_name', models.CharField(max_length=20)),
                ('app_version', models.PositiveIntegerField()),
                ('customer', models.ForeignKey(to='nwk.Consumer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='installation',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Installation',
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 7, 23, 4, 40, 196611)),
        ),
    ]
