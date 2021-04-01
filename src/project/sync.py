import logging
from uuid import UUID

from django.db.transaction import atomic

from connector.provider import connector_provider
from dependency.models import Dependency
from project.models import Project, ProjectDependency
from shared.mappers import SourceFileToLanguageMapper
from user_platform.models import UserPlatform


class Sync:
    _BATCH_SIZE = 100

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
        logging.info(f"Project {project_id} sync started.")
        project_dependency_versions = set()
        dependency_name_id_map = {
            f"{language}:{name}": index
            for index, name, language in Dependency.objects.values_list(
                Dependency.Fields.ID, Dependency.Fields.NAME, Dependency.Fields.LANGUAGE
            )
        }
        for dependency in self._connector.list_dependencies(project_id):
            language = SourceFileToLanguageMapper.map(dependency.source_type)
            index = dependency_name_id_map.get(f"{language}:{dependency.name}")
            if index is None:
                dep, created = Dependency.objects.get_or_create(
                    name=dependency.name,
                    language=language,
                )
                index = dep.id
                dependency_name_id_map[f"{language}:{dependency.name}"] = index
            project_dependency_versions.add(
                ProjectDependency(
                    dependency_id=index,
                    project_id=project_id,
                    version=dependency.version,
                    source_type=dependency.source_type,
                    source_file=dependency.source_file,
                )
            )
        project_dependencies_count = len(project_dependency_versions)
        ProjectDependency.objects.filter(project_id=project_id).delete()
        ProjectDependency.objects.bulk_create(
            objs=project_dependency_versions, batch_size=self._BATCH_SIZE
        )
        logging.info(
            f"Project {project_id} synced successfully with "
            f"{project_dependencies_count} dependencies."
        )
