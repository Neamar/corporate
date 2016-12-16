# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('engine', '0006_auto_20160615_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='last_update',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='password',
            field=models.CharField(default=datetime.datetime(2016, 6, 18, 21, 12, 32, 214668, tzinfo=utc), max_length=128),
            preserve_default=False,
        ),
    ]
