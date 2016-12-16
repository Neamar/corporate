# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stdimage.utils
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0004_auto_20160609_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='avatar',
            field=stdimage.models.StdImageField(upload_to=stdimage.utils.UploadToUUID(path=b'avatars')),
        ),
    ]
