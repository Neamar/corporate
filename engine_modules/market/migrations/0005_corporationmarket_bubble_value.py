# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20150802_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporationmarket',
            name='bubble_value',
            field=models.SmallIntegerField(default=0),
        ),
    ]
