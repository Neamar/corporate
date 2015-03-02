# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0001_initial'),
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporationSpeculationOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
                ('investment', models.PositiveIntegerField(help_text=b'En milliers de nuyens.')),
                ('on_win_ratio', models.PositiveSmallIntegerField(default=1, editable=False)),
                ('on_loss_ratio', models.PositiveSmallIntegerField(default=1, editable=False)),
                ('rank', models.PositiveSmallIntegerField()),
                ('corporation', models.ForeignKey(to='corporation.Corporation')),
            ],
            options={
                'abstract': False,
            },
            bases=('engine.order',),
        ),
    ]
