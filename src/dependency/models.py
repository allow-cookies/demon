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
        FROM_FILE = "from_file"

    name = CharField(max_length=255)
    version = CharField(max_length=31)
    project = ForeignKey(
        Project,
        on_delete=CASCADE,
        related_name=Project.Fields.DEPENDENCIES,
        related_query_name=Project.Fields.DEPENDENCIES,
    )
    from_file = CharField(max_length=127)

    def __str__(self):
        return self.name
