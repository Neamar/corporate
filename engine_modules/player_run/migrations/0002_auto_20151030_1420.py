# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
        ('player_run', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informationorder',
            name='target',
        ),
        migrations.AddField(
            model_name='informationorder',
            name='target',
            field=models.ManyToManyField(to='engine.Player'),
        ),
    ]
