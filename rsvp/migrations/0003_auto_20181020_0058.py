# Generated by Django 2.1.2 on 2018-10-20 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0002_auto_20181020_0049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='party',
        ),
        migrations.AddField(
            model_name='party',
            name='guests',
            field=models.ManyToManyField(to='rsvp.Guest'),
        ),
    ]