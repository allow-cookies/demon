from django.db.models import CASCADE, CharField, ForeignKey
from django.utils.translation import gettext_lazy as _

from project.models import Project
from shared.models import UUIDModel


class Dependency(UUIDModel):
    class Meta:
        verbose_name_plural = _("Dependencies")

    class Fields:
        NAME = "name"
        VERSION = "version"
        PROJECT = "project"
        SOURCE_FILE = "source_file"

    name = CharField(max_length=255)
    version = CharField(max_length=63)
    project = ForeignKey(
        Project,
        on_delete=CASCADE,
        related_name=Project.Fields.DEPENDENCIES,
        related_query_name=Project.Fields.DEPENDENCIES,
    )
    source_file = CharField(max_length=127)

    def __str__(self):
        return self.name
