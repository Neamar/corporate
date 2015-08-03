# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_auto_20150802_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporationmarket',
            name='turn',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
