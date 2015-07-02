# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_delete_globalpermission'),
        ('pydgin_auth', '0008_delete_globalpermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPermission',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name': 'global_permission',
            },
            bases=('auth.permission',),
        ),
    ]
