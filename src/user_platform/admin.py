from django.contrib.admin import ModelAdmin, register

from user_platform.models import UserPlatform


@register(UserPlatform)
class UserPlatformAdmin(ModelAdmin):
    list_display = (
        UserPlatform.Fields.USER,
        UserPlatform.Fields.PLATFORM,
        UserPlatform.Fields.URL,
    )
