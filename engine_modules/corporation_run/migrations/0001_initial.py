# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0001_initial'),
        ('market', '__first__'),
        ('corporation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporationRunOrder',
            fields=[
                ('runorder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='run.RunOrder')),
            ],
            options={
            },
            bases=('run.runorder',),
        ),
        migrations.CreateModel(
            name='CorporationRunOrderWithStealer',
            fields=[
                ('CorporationRunOrder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='corporation_run.CorporationRunOrder')),
            ],
            options={
            },
            bases=('corporation_run.CorporationRunOrder',),
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('CorporationRunOrderwithstealer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='corporation_run.CorporationRunOrderWithStealer')),
            ],
            options={
            },
            bases=('corporation_run.CorporationRunOrderwithstealer',),
        ),
        migrations.CreateModel(
            name='DataStealOrder',
            fields=[
                ('CorporationRunOrderwithstealer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='corporation_run.CorporationRunOrderWithStealer')),
            ],
            options={
            },
            bases=('corporation_run.CorporationRunOrderwithstealer',),
        ),
        migrations.CreateModel(
            name='ProtectionOrder',
            fields=[
                ('runorder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='run.RunOrder')),
                ('protected_corporation_market', models.ForeignKey(related_name='protectors', to='market.CorporationMarket')),
            ],
            options={
            },
            bases=('run.runorder',),
        ),
        migrations.CreateModel(
            name='SabotageOrder',
            fields=[
                ('CorporationRunOrder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='corporation_run.CorporationRunOrder')),
            ],
            options={
            },
            bases=('corporation_run.CorporationRunOrder',),
        ),
        migrations.AddField(
            model_name='CorporationRunOrderwithstealer',
            name='stealer_corporation',
            field=models.ForeignKey(related_name='+', to='corporation.Corporation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='CorporationRunOrder',
            name='target_corporation_market',
            field=models.ForeignKey(related_name='scoundrels', to='market.CorporationMarket'),
            preserve_default=True,
        ),
    ]
