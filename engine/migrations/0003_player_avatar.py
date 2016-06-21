# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0002_auto_20160102_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='avatar',
            field=models.ImageField(upload_to=b'avatar', blank=True),
        ),
    ]
