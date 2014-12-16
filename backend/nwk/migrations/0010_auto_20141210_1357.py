# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nwk', '0009_auto_20141007_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrabPromotion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('redeem_time', models.DateTimeField(auto_now=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('qr_code_url', models.URLField()),
                ('point', models.PositiveIntegerField()),
                ('customer', models.ForeignKey(to='nwk.Consumer')),
                ('promotion', models.ForeignKey(to='nwk.Promotion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mall',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('mall_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=60)),
                ('region', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='retail',
            name='mall',
            field=models.ForeignKey(default=1, to='nwk.Mall'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 13, 56, 38, 70516)),
        ),
    ]
