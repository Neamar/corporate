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
            name='VoteOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
                ('corporation_market_down', models.ForeignKey(related_name='+', to='market.CorporationMarket')),
                ('corporation_market_up', models.ForeignKey(related_name='+', to='market.CorporationMarket')),
            ],
            options={
            },
            bases=('engine.order',),
        ),
    ]
