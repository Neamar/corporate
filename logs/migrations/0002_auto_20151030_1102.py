# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='concernedplayer',
            unique_together=set([('player', 'log')]),
        ),
    ]
