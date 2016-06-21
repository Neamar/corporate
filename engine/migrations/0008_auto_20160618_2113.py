# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0007_auto_20160618_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='password',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
