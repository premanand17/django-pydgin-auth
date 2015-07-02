# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_delete_globalpermission'),
        ('pydgin_auth', '0010_delete_globalpermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPermission',
            fields=[
            ],
            options={
                'permissions': (('can_read_ic', 'Can read ImmunoChip'), ('can_read_gwas', 'Can read GWAS')),
                'proxy': True,
            },
            bases=('auth.permission',),
        ),
    ]
