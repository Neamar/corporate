# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '__first__'),
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetDelta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=15, choices=[(b'effect-first', b'Eff. premier'), (b'effect-last', b'Eff. dernier'), (b'effect-crash', b'Eff. crash'), (b'mdc', b'MDC'), (b'sabotage', b'Sabotage'), (b'extraction', b'Extraction'), (b'datasteal', b'Datasteal'), (b'invisible-hand', b'Main Invisible'), (b'votes', b'Votes')])),
                ('delta', models.SmallIntegerField()),
                ('turn', models.SmallIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_corporation_slug', models.CharField(max_length=20)),
                ('assets', models.SmallIntegerField()),
                ('game', models.ForeignKey(to='engine.Game')),
                ('historic_market', models.ForeignKey(to='market.Market')),
            ],
            options={
                'ordering': ['base_corporation_slug'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='corporation',
            unique_together=set([('base_corporation_slug', 'game')]),
        ),
        migrations.AddField(
            model_name='assetdelta',
            name='corporation',
            field=models.ForeignKey(to='corporation.Corporation'),
            preserve_default=True,
        ),
    ]
