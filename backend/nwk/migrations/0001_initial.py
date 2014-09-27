# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=5000)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('image_url', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PromotionDiscount',
            fields=[
                ('promotion_ptr', models.OneToOneField(auto_created=True, to='nwk.Promotion', serialize=False, primary_key=True, parent_link=True)),
                ('discount', models.PositiveSmallIntegerField()),
            ],
            options={
            },
            bases=('nwk.promotion',),
        ),
        migrations.CreateModel(
            name='PromotionGeneral',
            fields=[
                ('promotion_ptr', models.OneToOneField(auto_created=True, to='nwk.Promotion', serialize=False, primary_key=True, parent_link=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
            },
            bases=('nwk.promotion',),
        ),
        migrations.CreateModel(
            name='PromotionPriceReduction',
            fields=[
                ('promotion_ptr', models.OneToOneField(auto_created=True, to='nwk.Promotion', serialize=False, primary_key=True, parent_link=True)),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
            },
            bases=('nwk.promotion',),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('website', models.URLField(blank=True)),
                ('picture', models.URLField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
