# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0007_auto_20140927_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotion',
            name='grabbed_by',
        ),
        migrations.AddField(
            model_name='consumer',
            name='grabbed',
            field=models.ManyToManyField(to='nwk.Promotion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 27, 14, 41, 37, 888751)),
        ),
    ]
