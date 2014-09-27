# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0002_auto_20140920_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 20, 11, 25, 14, 106656), auto_now=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='time_expiry',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
