# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0009_auto_20160618_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='background',
            field=models.CharField(default=b'Anonyme', max_length=50, choices=[('Anonyme', 'Anonyme'), ('Acharn\xe9', 'Acharn\xe9'), ('Analyste', 'Analyste'), ('Altruisite', 'Altruisite'), ('Corrupteur', 'Corrupteur'), ('D\xe9vou\xe9', 'D\xe9vou\xe9'), ('Flambeur', 'Flambeur'), ('Grande geule', 'Grande geule'), ('Oligarque', 'Oligarque'), ('Pacifiste', 'Pacifiste'), ('Parano\xefaque', 'Parano\xefaque'), ('Protecteur', 'Protecteur'), ('Pyromane', 'Pyromane'), ('Tra\xeetre', 'Tra\xeetre'), ('Violent', 'Violent'), ('V\xe9nal', 'V\xe9nal')]),
        ),
    ]
