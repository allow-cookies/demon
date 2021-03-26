from django.contrib.admin import ModelAdmin, register

from dependency.models import Dependency


@register(Dependency)
class DependencyAdmin(ModelAdmin):
    list_display = (
        Dependency.Fields.NAME,
        Dependency.Fields.VERSION,
        Dependency.Fields.PROJECT,
        Dependency.Fields.FROM_FILE,
    )
    search_fields = (Dependency.Fields.NAME,)
    ordering = (Dependency.Fields.NAME,)
