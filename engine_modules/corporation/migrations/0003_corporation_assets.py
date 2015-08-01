# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0002_remove_corporation_assets'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporation',
            name='assets',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
