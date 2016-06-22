# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0010_auto_20160618_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='started',
        ),
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(default=b'created', max_length=50, choices=[('created', 'created'), ('started', 'started'), ('ended', 'ended')]),
        ),
    ]
