# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mdc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdcvoteorder',
            name='coalition',
            field=models.CharField(default=None, max_length=4, null=True, blank=True, choices=[(b'CPUB', b'Contrats publics'), (b'RSEC', 'R\xe9forme de la s\xe9curit\xe9'), (b'CONS', b'Consolidation')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mdcvotesession',
            name='coalition',
            field=models.CharField(default=None, max_length=4, null=True, blank=True, choices=[(b'CPUB', b'Contrats publics'), (b'RSEC', 'R\xe9forme de la s\xe9curit\xe9'), (b'CONS', b'Consolidation')]),
            preserve_default=True,
        ),
    ]
