# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporation_run', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='corporationrunorderwithstealer',
            old_name='CorporationRunOrder_ptr',
            new_name='corporationrunorder_ptr',
        ),
        migrations.RenameField(
            model_name='datastealorder',
            old_name='CorporationRunOrderwithstealer_ptr',
            new_name='corporationrunorderwithstealer_ptr',
        ),
        migrations.RenameField(
            model_name='extractionorder',
            old_name='CorporationRunOrderwithstealer_ptr',
            new_name='corporationrunorderwithstealer_ptr',
        ),
        migrations.RenameField(
            model_name='sabotageorder',
            old_name='CorporationRunOrder_ptr',
            new_name='corporationrunorder_ptr',
        ),
    ]
