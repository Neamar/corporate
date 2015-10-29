# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0004_corporation_crashed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corporation',
            name='crashed',
        ),
        migrations.AddField(
            model_name='corporation',
            name='crash_turn',
            field=models.SmallIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='corporation',
            name='game',
            field=models.ForeignKey(related_name='all_corporation_set', to='engine.Game'),
        ),
    ]
