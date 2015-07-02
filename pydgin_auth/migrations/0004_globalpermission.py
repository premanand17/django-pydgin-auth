# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('pydgin_auth', '0003_remove_userprofile_email'),
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
