# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0001_initial'),
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformationOrder',
            fields=[
                ('runorder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='run.RunOrder')),
                ('target', models.ForeignKey(to='engine.Player')),
            ],
            options={
            },
            bases=('run.runorder',),
        ),
    ]
