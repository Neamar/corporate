# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='engine.Order')),
                ('has_influence_bonus', models.BooleanField(default=False, help_text=b'Accorder \xc3\xa0 cette run une remise de 300k')),
                ('additional_percents', models.PositiveSmallIntegerField(default=1, help_text=b'Palier de 10% suppl\xc3\xa9mentaires.', validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)])),
                ('hidden_percents', models.SmallIntegerField(default=0, editable=False)),
            ],
            options={
            },
            bases=('engine.order',),
        ),
    ]
