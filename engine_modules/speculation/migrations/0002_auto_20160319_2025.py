# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speculation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporationspeculationorder',
            name='investment',
            field=models.PositiveIntegerField(help_text=b'En k\xe2\x82\xb5'),
        ),
    ]
