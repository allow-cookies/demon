from uuid import UUID

from celery import shared_task

from connector.provider import connector_provider
from project.sync import ProjectSync
from user_platform.models import UserPlatform


@shared_task
def sync_user_projects(user_id: UUID):
    platforms = UserPlatform.objects.filter(user_id=user_id)
    for platform in platforms:
        connector = connector_provider.provide(
            platform_name=platform.platform, user_id=user_id
        )
        ProjectSync(platform_connector=connector).execute()
