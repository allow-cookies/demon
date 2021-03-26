from typing import Generator
from uuid import UUID

import gitlab

from connector.base import PlatformConnector
from dependency.dto import DependencyDTO
from dependency.parser.provider import parser_provider
from project.dto import ProjectDTO
from project.models import Project
from user_platform.models import UserPlatform


class GitLabConnector(PlatformConnector):
    _PER_PAGE = 999
    _FIELD_NAME = "name"
    _FIELD_ID = "id"

    def __init__(self, user_id: UUID):
        super().__init__(user_id=user_id)
        url, token = self._fetch_credentials(user_id)
        self._api = gitlab.Gitlab(url, private_token=token)
        self._registered_dependency_file_types = (
            parser_provider.list_registered_file_types()
        )

    @staticmethod
    def _fetch_credentials(user_id: UUID) -> tuple[str, str]:
        return (
            UserPlatform.objects.filter(
                user_id=user_id, platform=str(UserPlatform.PlatformChoices.GITLAB)
            )
            .values_list(UserPlatform.Fields.URL, UserPlatform.Fields.TOKEN)
            .first()
        )

    def list_projects(self) -> Generator[ProjectDTO, None, None]:
        for group in self._api.groups.list(per_page=self._PER_PAGE):
            for project in group.projects.list(per_page=self._PER_PAGE):
                yield ProjectDTO(
                    external_id=project.id,
                    name=project.name,
                    path=project.path_with_namespace,
                    description=project.description,
                    created_at=project.created_at,
                    dependencies=set(),
                )

    def list_dependencies(
        self, project_id: UUID
    ) -> Generator[DependencyDTO, None, None]:
        external_project_id = (
            Project.objects.filter(id=project_id)
            .values_list(Project.Fields.EXTERNAL_ID, flat=True)
            .first()
        )
        project = self._api.projects.get(external_project_id, lazy=True)
        for item in project.repository_tree():
            if item[self._FIELD_NAME] in self._registered_dependency_file_types:
                contents = project.repository_raw_blob(item[self._FIELD_ID])
                parser = parser_provider.provide(item[self._FIELD_NAME])
                yield from parser.parse(
                    from_file=item[self._FIELD_NAME], contents=str(contents)
                )
        yield from ()
