# Generated by Django 2.1.2 on 2018-10-20 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0003_auto_20181020_0058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='party',
            old_name='guests',
            new_name='guest',
        ),
        migrations.AlterField(
            model_name='guest',
            name='notes',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
