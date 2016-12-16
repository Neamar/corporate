# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0003_auto_20160107_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='runorder',
            name='additional_percents',
        ),
        migrations.RemoveField(
            model_name='runorder',
            name='has_influence_bonus',
        ),
        migrations.RemoveField(
            model_name='runorder',
            name='hidden_percents',
        ),
    ]
