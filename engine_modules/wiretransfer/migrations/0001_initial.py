# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WiretransferOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
                ('amount', models.PositiveIntegerField(help_text=b'En milliers de nuyens')),
                ('recipient', models.ForeignKey(to='engine.Player')),
            ],
            bases=('engine.order',),
        ),
    ]
