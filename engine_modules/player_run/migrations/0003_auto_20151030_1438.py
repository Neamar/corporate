# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0007_auto_20151030_1102'),
        ('player_run', '0002_auto_20151030_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='informationorder',
            old_name='target',
            new_name='player_targets',
        ),
        migrations.AddField(
            model_name='informationorder',
            name='corporation_targets',
            field=models.ManyToManyField(to='corporation.Corporation'),
        ),
    ]
