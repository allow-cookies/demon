from __future__ import annotations

from django.contrib.admin import ModelAdmin, register

from user.models import User


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
