# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0008_auto_20160618_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='background',
            field=models.CharField(default=b'Anonyme', max_length=50, choices=[(b'ANO', 'Anonyme'), (b'VIO', 'Violent'), (b'PAC', 'Pacifiste'), (b'PRO', 'Protecteur'), (b'PRY', 'Pyromane'), (b'ACH', 'Acharn\xe9'), (b'FLA', 'Flambeur'), (b'ANA', 'Analyste'), (b'PAR', 'Parano\xefaque'), (b'OLI', 'Oligarque'), (b'DEV', 'D\xe9vou\xe9'), (b'GRA', 'Grande geule'), (b'TRA', 'Tra\xeetre'), (b'ALT', 'Altruisite'), (b'COR', 'Corrupteur'), (b'VEN', 'V\xe9nal')]),
        ),
    ]
