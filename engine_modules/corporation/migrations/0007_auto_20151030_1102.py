# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0006_auto_20150813_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetdelta',
            name='category',
            field=models.CharField(max_length=15, choices=[(b'effect-first', b'Eff. premier'), (b'effect-last', b'Eff. dernier'), (b'effect-crash', b'Eff. crash'), (b'detroit-inc', b'Detroit, Inc.'), (b'sabotage', b'Sabotage'), (b'extraction', b'Extraction'), (b'datasteal', b'Datasteal'), (b'market*bubble', b'Domination/Perte s\xc3\xa8che'), (b'invisible-hand', b'Main Invisible'), (b'votes', b'Votes')]),
        ),
    ]
