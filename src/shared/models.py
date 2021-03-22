from uuid import uuid4

from django.db.models import Model, UUIDField


class UUIDModel(Model):
    class Meta:
        abstract = True

    class Fields:
        ID = "id"

    id = UUIDField(primary_key=True, default=uuid4, editable=False)
