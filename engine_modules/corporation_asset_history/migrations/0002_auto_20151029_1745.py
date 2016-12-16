# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation_asset_history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assethistory',
            name='assets',
            field=models.SmallIntegerField(),
        ),
    ]
