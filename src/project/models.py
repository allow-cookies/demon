from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    TextChoices,
    TextField,
    UniqueConstraint,
)
from django.utils.translation import gettext_lazy as _

from dependency.models import Dependency
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


class ProjectDependency(UUIDModel):
    class Fields(UUIDModel.Fields):
        PROJECT = "project"
        DEPENDENCY = "dependency"
        VERSION = "version"
        SOURCE_FILE = "source_file"

    class SourceFileChoices(TextChoices):
        REQUIREMENTS_TXT = "requirements.txt", _("requirements.txt")
        PIPFILE_LOCK = "Pipfile.lock", _("Pipfile.lock")
        PACKAGE_LOCK_JSON = "package-lock.json", _("package-lock.json")
        YARN_LOCK = "yarn.lock", _("yarn.lock")

    version = CharField(max_length=63)
    dependency = ForeignKey(
        Dependency,
        on_delete=CASCADE,
        related_name=Dependency.Fields.VERSIONS,
        related_query_name=Dependency.Fields.VERSIONS,
    )
    project = ForeignKey(
        Project,
        on_delete=CASCADE,
        related_name=Project.Fields.DEPENDENCIES,
        related_query_name=Project.Fields.DEPENDENCIES,
    )
    source_file = CharField(max_length=63, choices=SourceFileChoices.choices)
