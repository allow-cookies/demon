from django.db.models import CharField, DateTimeField, TextField

from shared.models import UUIDModel


class Project(UUIDModel):
    class Fields(UUIDModel.Fields):
        EXTERNAL_ID = "external_id"
        NAME = "name"
        PATH = "path"
        DESCRIPTION = "description"
        CREATED_AT = "created_at"
        LAST_SCANNED_AT = "last_scanned_at"
        DEPENDENCIES = "dependencies"

    external_id = CharField(max_length=255)
    name = CharField(max_length=255)
    path = CharField(max_length=255)
    description = TextField(default="")
    created_at = DateTimeField()
    last_scanned_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.path
