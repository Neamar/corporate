# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0004_auto_20160909_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='runorder',
            name='additional_percents',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='runorder',
            name='has_influence_bonus',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='runorder',
            name='hidden_percents',
            field=models.SmallIntegerField(default=0, editable=False),
        ),
    ]
