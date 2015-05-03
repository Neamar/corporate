# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetDelta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=15, choices=[(b'effect-first', b'Eff. premier'), (b'effect-last', b'Eff. dernier'), (b'effect-crash', b'Eff. crash'), (b'detroit-inc', b'Detroit, Inc.'), (b'sabotage', b'Sabotage'), (b'extraction', b'Extraction'), (b'datasteal', b'Datasteal'), (b'invisible-hand', b'Main Invisible'), (b'votes', b'Votes')])),
                ('delta', models.SmallIntegerField()),
                ('turn', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_corporation_slug', models.CharField(max_length=20)),
                ('assets', models.SmallIntegerField()),
                ('market_assets', models.SmallIntegerField()),
                ('assets_modifier', models.SmallIntegerField(default=0)),
                ('game', models.ForeignKey(to='engine.Game')),
            ],
            options={
                'ordering': ['base_corporation_slug'],
            },
        ),
        migrations.AddField(
            model_name='assetdelta',
            name='corporation',
            field=models.ForeignKey(to='corporation.Corporation'),
        ),
        migrations.AlterUniqueTogether(
            name='corporation',
            unique_together=set([('base_corporation_slug', 'game')]),
        ),
    ]
