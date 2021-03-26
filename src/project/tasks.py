from uuid import UUID

from celery import shared_task

from project.sync import Sync


@shared_task
def sync_platform_projects(platform_id: UUID):
    Sync(platform_id=platform_id).projects()
