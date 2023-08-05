# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-16 23:07
from __future__ import unicode_literals

from django.db import migrations

from kolibri.core.auth.constants.role_kinds import ADMIN


def device_owner_to_super_user(apps, schema_editor):
    from kolibri.core.auth.models import (
        FacilityUser as RealFacilityUser,
        Facility as RealFacility,
        Role as RealRole,
    )

    # The get_default_facility method now requires database access to another model that does not exist yet for
    # this migration, so just defer to the old behaviour.

    # Can't do much if no facilities exist, as no facility to FK the users onto
    if RealFacility.objects.exists():
        facility = RealFacility.objects.values("id", "dataset_id")[0]
        DeviceOwner = apps.get_model("kolibriauth", "DeviceOwner")
        FacilityUser = apps.get_model("kolibriauth", "FacilityUser")
        Facility = apps.get_model("kolibriauth", "Facility")
        default_facility = Facility.objects.get(pk=facility["id"])
        DevicePermissions = apps.get_model("device", "DevicePermissions")
        DeviceSettings = apps.get_model("device", "DeviceSettings")
        Role = apps.get_model("kolibriauth", "Role")
        for device_owner in DeviceOwner.objects.all():
            dataset_id = facility["dataset_id"]
            real_superuser = RealFacilityUser(
                username=device_owner.username,
                facility_id=facility["id"],
                dataset_id=dataset_id,
            )
            uuid = real_superuser.calculate_uuid()
            # due to uniqueness constraints, can't have two users with same username for a facility
            # so we end up only keeping the superuser
            FacilityUser.objects.filter(username=device_owner.username).delete()
            superuser = FacilityUser.objects.create(
                username=device_owner.username,
                password=device_owner.password,
                facility=default_facility,
                full_name=device_owner.full_name,
                date_joined=device_owner.date_joined,
                id=uuid,
                dataset_id=dataset_id,
                _morango_source_id=real_superuser._morango_source_id,
                _morango_partition=real_superuser._morango_partition,
            )
            real_role = RealRole(
                user_id=superuser.id,
                collection_id=facility["id"],
                kind=ADMIN,
                dataset_id=dataset_id,
            )
            role_uuid = real_role.calculate_uuid()
            Role.objects.create(
                user=superuser,
                collection=default_facility,
                kind=ADMIN,
                id=role_uuid,
                dataset_id=dataset_id,
                _morango_source_id=real_role._morango_source_id,
                _morango_partition=real_role._morango_partition,
            )
            DevicePermissions.objects.create(user=superuser, is_superuser=True)
        # Finally, set the is_provisioned flag
        settings, created = DeviceSettings.objects.get_or_create(is_provisioned=True)


class Migration(migrations.Migration):

    dependencies = [
        ("kolibriauth", "0003_auto_20170621_0958"),
        ("device", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(device_owner_to_super_user, migrations.RunPython.noop),
        migrations.DeleteModel(name="DeviceOwner"),
    ]
