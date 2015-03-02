# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assets', models.PositiveSmallIntegerField()),
                ('turn', models.PositiveSmallIntegerField()),
                ('corporation', models.ForeignKey(to='corporation.Corporation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='assethistory',
            unique_together=set([('corporation', 'turn')]),
        ),
    ]
