# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20150809_1404'),
        ('corporation', '0003_corporation_assets'),
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcernedPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transmittable', models.BooleanField()),
                ('personal', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turn', models.PositiveSmallIntegerField()),
                ('delta', models.SmallIntegerField()),
                ('hide_for_players', models.BooleanField()),
                ('public', models.BooleanField()),
                ('event_type', models.CharField(max_length=30)),
                ('data', models.TextField()),
                ('corporation', models.ForeignKey(to='corporation.Corporation', null=True)),
                ('corporation_market', models.ForeignKey(to='market.CorporationMarket', null=True)),
                ('game', models.ForeignKey(to='engine.Game')),
                ('players', models.ManyToManyField(to='engine.Player', through='logs.ConcernedPlayer')),
            ],
        ),
        migrations.AddField(
            model_name='concernedplayer',
            name='log',
            field=models.ForeignKey(to='logs.Log'),
        ),
        migrations.AddField(
            model_name='concernedplayer',
            name='player',
            field=models.ForeignKey(to='engine.Player'),
        ),
    ]
