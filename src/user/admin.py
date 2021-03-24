from __future__ import annotations

from django.contrib.admin import register, ModelAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from user.models import User
from user.tasks import sync_user_projects


def perform_sync(modeladmin: UserAdmin, request: WSGIRequest, queryset: QuerySet):
    user_ids = queryset.values_list(User.Fields.ID, flat=True)
    for user_id in user_ids:
        print(user_id)
        sync_user_projects.delay(user_id=user_id)


@register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        User.Fields.EMAIL,
        User.Fields.IS_ACTIVE,
        User.Fields.IS_SUPERUSER,
        User.Fields.LAST_LOGIN,
    )
    list_filter = (
        User.Fields.IS_SUPERUSER,
        User.Fields.IS_ADMIN,
        User.Fields.IS_ACTIVE,
    )
    actions = (perform_sync,)
