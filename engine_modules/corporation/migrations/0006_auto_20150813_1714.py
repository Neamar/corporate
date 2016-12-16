# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0005_auto_20150813_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporation',
            name='crash_turn',
            field=models.SmallIntegerField(null=True, blank=True),
        ),
    ]
