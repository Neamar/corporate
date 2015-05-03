# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
        ('corporation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporationMarket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField()),
                ('corporation', models.ForeignKey(to='corporation.Corporation')),
            ],
            options={
                'ordering': ['corporation', 'market'],
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('game', models.ForeignKey(to='engine.Game')),
            ],
        ),
        migrations.AddField(
            model_name='corporationmarket',
            name='market',
            field=models.ForeignKey(to='market.Market'),
        ),
        migrations.AlterUniqueTogether(
            name='market',
            unique_together=set([('game', 'name')]),
        ),
    ]
