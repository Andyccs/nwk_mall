# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(auto_now=True, default=datetime.date(2014, 9, 20)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='promotion',
            name='time_expiry',
            field=models.DateTimeField(default=datetime.date(2014, 9, 20)),
            preserve_default=False,
        ),
    ]
