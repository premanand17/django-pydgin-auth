# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pydgin_auth', '0007_auto_20150626_1413'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GlobalPermission',
        ),
    ]
