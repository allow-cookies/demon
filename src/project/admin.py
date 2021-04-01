from __future__ import annotations

from django.contrib.admin import ModelAdmin, register
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from dependency.models import Dependency
from dependency.tasks import sync_project_dependencies
from project.models import Project, ProjectDependency


def synchronize_project_dependencies(
    modeladmin: ProjectAdmin, request: WSGIRequest, queryset: QuerySet
):
    project_ids = queryset.values_list(Project.Fields.ID, flat=True)
    for project_id in project_ids:
        sync_project_dependencies.delay(project_id=project_id)


@register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        Project.Fields.NAME,
        Project.Fields.PATH,
        Project.Fields.DESCRIPTION,
        Project.Fields.CREATED_AT,
        Project.Fields.LAST_SCANNED_AT,
        Project.Fields.PLATFORM,
    )
    search_fields = (
        Project.Fields.NAME,
        Project.Fields.DESCRIPTION,
        Project.Fields.PATH,
    )
    ordering = (Project.Fields.PATH,)
    actions = (synchronize_project_dependencies,)


@register(ProjectDependency)
class ProjectDependencyAdmin(ModelAdmin):
    list_display = (
        ProjectDependency.Fields.PROJECT,
        ProjectDependency.Fields.DEPENDENCY,
        ProjectDependency.Fields.VERSION,
        ProjectDependency.Fields.SOURCE_FILE,
    )
    list_filter = (
        ProjectDependency.Fields.SOURCE_FILE,
    )
    search_fields = (
        f"{ProjectDependency.Fields.PROJECT}__{Project.Fields.NAME}",
        f"{ProjectDependency.Fields.DEPENDENCY}__{Dependency.Fields.NAME}",
    )
