# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0014_auto_20160629_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerPoints',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turn', models.PositiveSmallIntegerField(default=0)),
                ('total_points', models.SmallIntegerField(default=0)),
                ('share_points', models.SmallIntegerField(default=0)),
                ('citizenship_points', models.SmallIntegerField(default=0)),
                ('background_points', models.SmallIntegerField(default=0)),
                ('dinc_points', models.SmallIntegerField(default=0)),
                ('player', models.ForeignKey(to='engine.Player')),
            ],
        ),
    ]
