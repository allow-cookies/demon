from django.conf import settings
from django.db.models import PROTECT, CharField, ForeignKey, TextChoices, URLField
from django.utils.translation import gettext_lazy as _

from shared.models import UUIDModel
from user.models import User


class UserPlatform(UUIDModel):
    class Fields(UUIDModel.Fields):
        USER = "user"
        PLATFORM = "platform"
        URL = "url"
        TOKEN = "token"
        PROJECTS = "projects"

    class PlatformChoices(TextChoices):
        GITHUB = "GITHUB", _("Github")
        GITLAB = "GITLAB", _("GitLab")
        BITBUCKET = "BITBUCKET", _("Bitbucket")

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        related_name=User.Fields.PLATFORMS,
        related_query_name=User.Fields.PLATFORMS,
    )
    platform = CharField(max_length=31, choices=PlatformChoices.choices)
    url = URLField(max_length=255)
    token = CharField(max_length=255)

    def __str__(self) -> str:
        return f"[{self.platform}] {self.url}"
