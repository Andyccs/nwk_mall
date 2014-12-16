# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0011_auto_20141210_1357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grabpromotion',
            old_name='customer',
            new_name='consumer',
        ),
        migrations.RemoveField(
            model_name='consumer',
            name='grabbed',
        ),
        migrations.AlterField(
            model_name='consumer',
            name='favorite_shops',
            field=models.ManyToManyField(blank=True, to='nwk.Retail'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 16, 4, 4, 42, 991479)),
        ),
    ]
