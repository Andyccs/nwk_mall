# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0013_auto_20141216_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 16, 4, 5, 18, 823970)),
        ),
    ]
