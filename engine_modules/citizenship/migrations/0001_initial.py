# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
        ('corporation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citizenship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turn', models.PositiveSmallIntegerField(default=0)),
                ('corporation', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='corporation.Corporation', null=True)),
                ('player', models.ForeignKey(to='engine.Player')),
            ],
        ),
        migrations.CreateModel(
            name='CitizenshipOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
                ('corporation', models.ForeignKey(to='corporation.Corporation')),
            ],
            bases=('engine.order',),
        ),
    ]
