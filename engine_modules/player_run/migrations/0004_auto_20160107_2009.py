# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player_run', '0003_auto_20151030_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationorder',
            name='corporation_targets',
            field=models.ManyToManyField(to='corporation.Corporation', blank=True),
        ),
        migrations.AlterField(
            model_name='informationorder',
            name='player_targets',
            field=models.ManyToManyField(to='engine.Player', blank=True),
        ),
    ]
