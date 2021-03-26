from __future__ import annotations

from django.contrib.admin import ModelAdmin, register
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from project.tasks import sync_platform_projects
from user_platform.models import UserPlatform


def synchronize_platform_projects(
    modeladmin: UserPlatformAdmin, request: WSGIRequest, queryset: QuerySet
):
    platform_ids = queryset.values_list(UserPlatform.Fields.ID, flat=True)
    for platform_id in platform_ids:
        sync_platform_projects.delay(platform_id=platform_id)


@register(UserPlatform)
class UserPlatformAdmin(ModelAdmin):
    list_display = (
        UserPlatform.Fields.USER,
        UserPlatform.Fields.PLATFORM,
        UserPlatform.Fields.URL,
    )
    actions = (synchronize_platform_projects,)
