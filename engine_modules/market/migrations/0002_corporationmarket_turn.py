# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporationmarket',
            name='turn',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
