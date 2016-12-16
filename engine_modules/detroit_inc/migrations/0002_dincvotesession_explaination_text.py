# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detroit_inc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dincvotesession',
            name='explaination_text',
            field=models.TextField(null=True, editable=False),
        ),
    ]
