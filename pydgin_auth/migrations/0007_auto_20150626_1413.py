# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pydgin_auth', '0006_globalpermission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='globalpermission',
            options={'verbose_name': 'global_permission'},
        ),
    ]
