# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0005_auto_20161108_1033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='runorder',
            old_name='has_influence_bonus',
            new_name='has_RSEC_bonus',
        ),
    ]
