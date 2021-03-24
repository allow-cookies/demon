from connector.base import PlatformConnector
from dependency.models import Dependency
from project.models import Project


class ProjectSync:
    def __init__(self, platform_connector: PlatformConnector):
        self._connector = platform_connector

    def execute(self):
        for project_dto in self._connector.list_projects():
            project, created = Project.objects.update_or_create(
                external_id=project_dto.external_id,
                defaults={
                    "name": project_dto.name,
                    "path": project_dto.path,
                    "description": project_dto.description,
                    "created_at": project_dto.created_at,
                },
            )
            Dependency.objects.filter(project_id=project.id).delete()
            Dependency.objects.bulk_create(
                [
                    Dependency(
                        name=dependency.name,
                        version=dependency.version,
                        from_file=dependency.from_file,
                        project=project,
                    )
                    for dependency in project_dto.dependencies
                ]
            )
