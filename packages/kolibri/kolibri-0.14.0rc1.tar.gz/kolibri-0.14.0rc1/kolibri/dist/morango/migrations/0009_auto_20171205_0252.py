# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-12-05 08:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("morango", "0008_auto_20171114_2217")]

    operations = [
        migrations.RenameField(
            model_name="instanceidmodel", old_name="macaddress", new_name="node_id"
        )
    ]
