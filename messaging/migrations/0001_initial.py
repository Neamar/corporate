# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
        ('market', '__first__'),
        ('corporation', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('content', models.TextField(blank=True)),
                ('flag', models.CharField(max_length=3, choices=[(b'PM', b'Message priv\xc3\xa9'), (b'RE', b'R\xc3\xa9solution'), (b'CT', b"Envoi d'argent")])),
                ('turn', models.PositiveSmallIntegerField()),
                ('author', models.ForeignKey(related_name='+', to='engine.Player', null=True)),
                ('recipient_set', models.ManyToManyField(to='engine.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Newsfeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=15, choices=[(b'1-mdc', b'Bulletin du MDC'), (b'4-matrix-buzz', b'Matrix Buzz'), (b'3-people', b'Flash People'), (b'2-economy', b'\xc3\x89conomie')])),
                ('content', models.TextField(blank=True)),
                ('turn', models.PositiveSmallIntegerField()),
                ('path', models.CharField(max_length=250, blank=True)),
                ('status', models.CharField(default=b'public', max_length=15, choices=[(b'public', b'Information publique'), (b'private', b'Information priv\xc3\xa9e'), (b'public anonymous', b'Information anonymis\xc3\xa9e mais publique')])),
                ('corporations', models.ManyToManyField(to='corporation.Corporation')),
                ('game', models.ForeignKey(to='engine.Game')),
                ('market', models.ForeignKey(to='market.Market', null=True)),
                ('players', models.ManyToManyField(to='engine.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(default=b'global', max_length=15, choices=[(b'global', 'Global'), (b'runs', 'Runs'), (b'mdc', 'MDC'), (b'speculation', 'Sp\xe9culations'), (b'dividend', 'Dividendes')])),
                ('content', models.TextField(blank=True)),
                ('turn', models.PositiveSmallIntegerField()),
                ('recipient_set', models.ManyToManyField(to='engine.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
