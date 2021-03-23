# Generated by Django 3.1.7 on 2021-03-23 12:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("external_id", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("path", models.CharField(max_length=255)),
                ("description", models.TextField(default="")),
                ("created_at", models.DateTimeField()),
                ("last_scanned_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
