# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0001_initial'),
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CitizenShip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('corporation', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='corporation.Corporation', null=True)),
                ('player', models.OneToOneField(to='engine.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CitizenShipOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
                ('corporation', models.ForeignKey(to='corporation.Corporation')),
            ],
            options={
            },
            bases=('engine.order',),
        ),
    ]
