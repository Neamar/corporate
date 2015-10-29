# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0003_corporation_assets'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporation',
            name='crashed',
            field=models.BooleanField(default=False),
        ),
    ]
