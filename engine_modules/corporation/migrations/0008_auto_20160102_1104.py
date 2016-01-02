# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation', '0007_auto_20151029_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assetdelta',
            name='corporation',
        ),
        migrations.DeleteModel(
            name='AssetDelta',
        ),
    ]
