# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0002_auto_20160102_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runorder',
            name='additional_percents',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='runorder',
            name='has_influence_bonus',
            field=models.BooleanField(default=False, help_text=b'Accorder \xc3\xa0 cette run une remise de 300k', editable=False),
        ),
    ]
