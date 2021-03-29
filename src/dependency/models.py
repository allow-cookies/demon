from django.db.models import CharField, TextChoices
from django.utils.translation import gettext_lazy as _

from shared.models import UUIDModel


class Dependency(UUIDModel):
    class Meta:
        verbose_name_plural = _("Dependencies")

    class Fields(UUIDModel.Fields):
        NAME = "name"
        VERSIONS = "versions"
        LANGUAGE = "language"

    class DependencyLanguageChoices(TextChoices):
        PYTHON = "PYTHON", _("Python")
        JAVASCRIPT = "JAVASCRIPT", _("JavaScript")
        PHP = "PHP", _("PHP")

    name = CharField(max_length=255)
    language = CharField(max_length=15)

    def __str__(self):
        return self.name
