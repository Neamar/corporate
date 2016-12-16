# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_auto_20150804_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporationmarket',
            name='bubble_value',
            field=models.SmallIntegerField(default=0, choices=[(1, b'Bulle de domination'), (0, b'Pas de bulle'), (-1, b'Bulle n\xc3\xa9gative')]),
        ),
    ]
