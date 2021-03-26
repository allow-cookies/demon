from uuid import UUID

from celery import shared_task

from project.models import Project
from project.sync import Sync


@shared_task
def sync_project_dependencies(project_id: UUID):
    platform_id = (
        Project.objects.filter(pk=project_id)
        .values_list(Project.Fields.PLATFORM, flat=True)
        .first()
    )
    Sync(platform_id=platform_id).dependencies(project_id=project_id)
