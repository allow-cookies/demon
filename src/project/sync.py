from uuid import UUID

from django.db.transaction import atomic

from connector.provider import connector_provider
from dependency.models import Dependency
from project.models import Project
from user_platform.models import UserPlatform


class Sync:
    def __init__(self, platform_id: UUID):
        platform = UserPlatform.objects.get(id=platform_id)
        self._platform_id = platform_id
        self._connector = connector_provider.provide(
            platform_name=platform.platform, user_id=platform.user_id
        )

    def projects(self):
        # TODO: should be replaced with batch insert/update
        for project_dto in self._connector.list_projects():
            Project.objects.update_or_create(
                external_id=project_dto.external_id,
                platform_id=self._platform_id,
                defaults={
                    Project.Fields.NAME: project_dto.name,
                    Project.Fields.PATH: project_dto.path,
                    Project.Fields.DESCRIPTION: project_dto.description or "",
                    Project.Fields.CREATED_AT: project_dto.created_at,
                },
            )

    @atomic
    def dependencies(self, project_id: UUID):
        Dependency.objects.filter(project_id=project_id).delete()
        Dependency.objects.bulk_create(
            Dependency(
                name=dependency.name,
                version=dependency.version,
                from_file=dependency.from_file,
                project_id=project_id,
            )
            for dependency in self._connector.list_dependencies(project_id)
        )
