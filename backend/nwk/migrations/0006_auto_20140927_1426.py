# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0005_auto_20140927_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='installation',
            name='timezone',
            field=models.CharField(max_length=20, default='Asia/Singapore'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 27, 14, 26, 35, 924161)),
        ),
    ]
