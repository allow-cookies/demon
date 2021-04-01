# Generated by Django 3.1.7 on 2021-03-31 21:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dependency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('path', models.CharField(max_length=255)),
                ('description', models.TextField(default='')),
                ('created_at', models.DateTimeField()),
                ('last_scanned_at', models.DateTimeField(auto_now=True)),
                ('sync_enabled', models.BooleanField(default=False)),
                ('default_branch', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDependency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=63)),
                ('source_file', models.CharField(max_length=63)),
                ('source_type', models.CharField(choices=[('requirements.txt', 'requirements.txt'), ('Pipfile.lock', 'Pipfile.lock'), ('package-lock.json', 'package-lock.json'), ('yarn.lock', 'yarn.lock')], max_length=63)),
                ('dependency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', related_query_name='versions', to='dependency.dependency')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependencies', related_query_name='dependencies', to='project.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
