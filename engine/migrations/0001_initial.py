# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=50)),
                ('current_turn', models.PositiveSmallIntegerField(default=1)),
                ('total_turn', models.PositiveSmallIntegerField(default=8)),
                ('disable_side_effects', models.BooleanField(default=False, help_text=b'Disable all side effects (invisible hand, first and last effects, ...)')),
                ('started', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turn', models.PositiveSmallIntegerField(editable=False)),
                ('cost', models.PositiveSmallIntegerField(editable=False)),
                ('type', models.CharField(max_length=40, editable=False, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('money', models.PositiveIntegerField(default=2000)),
                ('background', models.CharField(max_length=50)),
                ('rp', models.TextField(default=b'', blank=True)),
                ('secrets', models.TextField(default=b'', blank=True)),
                ('game', models.ForeignKey(to='engine.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='player',
            field=models.ForeignKey(to='engine.Player'),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('game', 'user')]),
        ),
    ]
