# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corporation',
            name='historic_market',
        ),
        migrations.AddField(
            model_name='corporation',
            name='assets_modifier',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='corporation',
            name='market_assets',
            field=models.SmallIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='corporation',
            name='assets',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
