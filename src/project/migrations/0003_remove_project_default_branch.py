# Generated by Django 3.1.7 on 2021-03-31 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20210331_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='default_branch',
        ),
    ]