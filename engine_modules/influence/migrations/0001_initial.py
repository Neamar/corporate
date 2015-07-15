# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyInfluenceOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
            ],
            bases=('engine.order',),
        ),
        migrations.CreateModel(
            name='Influence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turn', models.PositiveSmallIntegerField(default=1)),
                ('level', models.PositiveSmallIntegerField(default=1)),
                ('player', models.ForeignKey(to='engine.Player')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='influence',
            unique_together=set([('player', 'turn')]),
        ),
    ]
