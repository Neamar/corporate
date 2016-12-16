# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0003_player_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='avatar',
            field=stdimage.models.StdImageField(upload_to=b'path/to/img'),
        ),
    ]
