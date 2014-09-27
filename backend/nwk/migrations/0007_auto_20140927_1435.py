# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0006_auto_20140927_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='retail',
            field=models.ForeignKey(to='nwk.Retail', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 27, 14, 35, 39, 636260)),
        ),
    ]
