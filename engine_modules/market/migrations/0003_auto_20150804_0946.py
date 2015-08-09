# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_corporationmarket_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporationmarket',
            name='bubble_value',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='corporationmarket',
            name='turn',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
