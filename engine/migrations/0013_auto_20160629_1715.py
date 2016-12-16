# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0012_auto_20160628_0609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cancellable',
        ),
        migrations.RemoveField(
            model_name='player',
            name='starting_citizenship',
        ),
        migrations.AlterField(
            model_name='player',
            name='background',
            field=models.CharField(default=b'Anonyme', max_length=50, choices=[('Anonyme', 'Anonyme'), ('Acharn\xe9', 'Acharn\xe9'), ('Analyste', 'Analyste'), ('Altruisite', 'Altruisite'), ('Corrupteur', 'Corrupteur'), ('D\xe9vou\xe9', 'D\xe9vou\xe9'), ('Flambeur', 'Flambeur'), ('Grande geule', 'Grande geule'), ('Oligarque', 'Oligarque'), ('Pacifiste', 'Pacifiste'), ('Parano\xefaque', 'Parano\xefaque'), ('Protecteur', 'Protecteur'), ('Pyromane', 'Pyromane'), ('Tra\xeetre', 'Tra\xeetre'), ('Violent', 'Violent'), ('V\xe9nal', 'V\xe9nal')]),
        ),
    ]
