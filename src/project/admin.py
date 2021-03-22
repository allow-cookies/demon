from django.contrib.admin import ModelAdmin, register

from project.models import Project


@register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        Project.Fields.NAME,
        Project.Fields.PATH,
        Project.Fields.DESCRIPTION,
        Project.Fields.CREATED_AT,
        Project.Fields.LAST_SCANNED_AT,
    )
    search_fields = (
        Project.Fields.NAME,
        Project.Fields.DESCRIPTION,
    )
    ordering = (Project.Fields.PATH,)
