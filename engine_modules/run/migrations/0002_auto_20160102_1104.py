# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runorder',
            name='additional_percents',
            field=models.SmallIntegerField(default=0, help_text=b'Palier de 10% suppl\xc3\xa9mentaires.', validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)]),
        ),
    ]
