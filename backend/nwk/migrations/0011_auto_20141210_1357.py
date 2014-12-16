# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0010_auto_20141210_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 13, 57, 36, 187379)),
        ),
    ]
