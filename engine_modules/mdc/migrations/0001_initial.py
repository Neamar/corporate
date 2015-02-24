# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MDCVoteOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
                ('coalition', models.CharField(default=None, max_length=4, null=True, blank=True, choices=[(b'CPUB', b'Contrats publics'), (b'OPCL', 'Op\xe9rations clandestines'), (b'CONS', b'Consolidation')])),
            ],
            options={
            },
            bases=('engine.order',),
        ),
        migrations.CreateModel(
            name='MDCVoteSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coalition', models.CharField(default=None, max_length=4, null=True, blank=True, choices=[(b'CPUB', b'Contrats publics'), (b'OPCL', 'Op\xe9rations clandestines'), (b'CONS', b'Consolidation')])),
                ('turn', models.PositiveSmallIntegerField(editable=False)),
                ('game', models.ForeignKey(to='engine.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
