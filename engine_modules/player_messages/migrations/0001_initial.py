# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0014_auto_20160629_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=300)),
                ('read', models.BooleanField(default=False)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(related_name='receiver', to='engine.Player')),
                ('sender', models.ForeignKey(related_name='sender', to='engine.Player')),
            ],
        ),
    ]