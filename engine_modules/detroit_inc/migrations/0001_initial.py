# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DIncVoteOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
                ('coalition', models.CharField(default=None, max_length=4, null=True, blank=True, choices=[(b'CPUB', b'Contrats publics'), (b'RSEC', 'R\xe9forme de la s\xe9curit\xe9'), (b'CONS', b'Consolidation')])),
            ],
            bases=('engine.order',),
        ),
        migrations.CreateModel(
            name='DIncVoteSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coalition', models.CharField(default=None, max_length=4, null=True, blank=True, choices=[(b'CPUB', b'Contrats publics'), (b'RSEC', 'R\xe9forme de la s\xe9curit\xe9'), (b'CONS', b'Consolidation')])),
                ('turn', models.PositiveSmallIntegerField(editable=False)),
                ('game', models.ForeignKey(to='engine.Game')),
            ],
        ),
    ]
