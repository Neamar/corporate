# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0005_auto_20160613_0523'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 15, 17, 48, 56, 82696, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='started',
            field=models.BooleanField(default=False),
        ),
    ]
