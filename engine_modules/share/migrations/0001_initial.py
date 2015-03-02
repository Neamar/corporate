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
            name='BuyShareOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
                ('corporation', models.ForeignKey(to='corporation.Corporation')),
            ],
            options={
            },
            bases=('engine.order',),
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turn', models.PositiveSmallIntegerField()),
                ('corporation', models.ForeignKey(to='corporation.Corporation')),
                ('player', models.ForeignKey(to='engine.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
