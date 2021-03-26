from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    TextField,
    UniqueConstraint,
)

from shared.models import UUIDModel
from user_platform.models import UserPlatform


class Project(UUIDModel):
    class Fields(UUIDModel.Fields):
        EXTERNAL_ID = "external_id"
        NAME = "name"
        PATH = "path"
        DESCRIPTION = "description"
        CREATED_AT = "created_at"
        LAST_SCANNED_AT = "last_scanned_at"
        DEPENDENCIES = "dependencies"
        SYNC_ENABLED = "sync_enabled"
        PLATFORM = "platform"

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("platform", "external_id"), name="platform_external_id_uniq"
            ),
        )

    external_id = CharField(max_length=255)
    name = CharField(max_length=255)
    path = CharField(max_length=255)
    description = TextField(default="")
    created_at = DateTimeField()
    last_scanned_at = DateTimeField(auto_now=True)
    sync_enabled = BooleanField(default=False)
    platform = ForeignKey(
        UserPlatform,
        on_delete=CASCADE,
        related_name=UserPlatform.Fields.PROJECTS,
        related_query_name=UserPlatform.Fields.PROJECTS,
    )

    def __str__(self):
        return self.path
