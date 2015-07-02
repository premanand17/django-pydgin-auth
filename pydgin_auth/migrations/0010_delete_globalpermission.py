# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pydgin_auth', '0009_globalpermission'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GlobalPermission',
        ),
    ]
