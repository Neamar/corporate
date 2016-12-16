# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='total_turn',
            field=models.PositiveSmallIntegerField(default=7),
        ),
        migrations.AlterField(
            model_name='player',
            name='background',
            field=models.CharField(default=b'Anonyme', max_length=50),
        ),
    ]
