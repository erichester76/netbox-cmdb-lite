# Generated by Django 5.0.10 on 2024-12-29 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_cmdb_lite', '0004_rename_deacription_genericobject_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericobjecttype',
            name='relationships',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]