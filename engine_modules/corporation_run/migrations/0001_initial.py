# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0001_initial'),
        ('market', '0001_initial'),
        ('corporation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporationRunOrder',
            fields=[
                ('runorder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='run.RunOrder')),
            ],
            bases=('run.runorder',),
        ),
        migrations.CreateModel(
            name='ProtectionOrder',
            fields=[
                ('runorder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='run.RunOrder')),
                ('protected_corporation_market', models.ForeignKey(related_name='protectors', to='market.CorporationMarket')),
            ],
            bases=('run.runorder',),
        ),
        migrations.CreateModel(
            name='CorporationRunOrderWithStealer',
            fields=[
                ('corporationrunorder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='corporation_run.CorporationRunOrder')),
            ],
            bases=('corporation_run.corporationrunorder',),
        ),
        migrations.CreateModel(
            name='SabotageOrder',
            fields=[
                ('corporationrunorder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='corporation_run.CorporationRunOrder')),
            ],
            bases=('corporation_run.corporationrunorder',),
        ),
        migrations.AddField(
            model_name='corporationrunorder',
            name='target_corporation_market',
            field=models.ForeignKey(related_name='scoundrels', to='market.CorporationMarket'),
        ),
        migrations.CreateModel(
            name='DataStealOrder',
            fields=[
                ('corporationrunorderwithstealer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='corporation_run.CorporationRunOrderWithStealer')),
            ],
            bases=('corporation_run.corporationrunorderwithstealer',),
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('corporationrunorderwithstealer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='corporation_run.CorporationRunOrderWithStealer')),
            ],
            bases=('corporation_run.corporationrunorderwithstealer',),
        ),
        migrations.AddField(
            model_name='corporationrunorderwithstealer',
            name='stealer_corporation',
            field=models.ForeignKey(related_name='+', to='corporation.Corporation'),
        ),
    ]
