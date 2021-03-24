from typing import Generator
from uuid import UUID

from django.conf import settings

import gitlab

from connector.base import PlatformConnector
from dependency.dto import DependencyDTO
from dependency.parser.provider import parser_provider
from project.dto import ProjectDTO
from user_platform.models import UserPlatform


class GitLabConnector(PlatformConnector):
    PER_PAGE = 100

    def __init__(self, user_id: UUID):
        super().__init__(user_id=user_id)
        url, token = self._fetch_credentials(user_id)
        self._api = gitlab.Gitlab(url, private_token=token)
        self._registered_dependency_file_types = (
            parser_provider.list_registered_file_types()
        )

    @staticmethod
    def _fetch_credentials(user_id: UUID) -> tuple[str, str]:
        return UserPlatform.objects.filter(
            user_id=user_id, platform=UserPlatform.PlatformChoices.GITLAB.name
        ).values_list(UserPlatform.Fields.URL, UserPlatform.Fields.TOKEN).first()

    def list_projects(self) -> Generator[ProjectDTO, None, None]:
        for group in self._api.groups.list(per_page=self.PER_PAGE):
            for project in group.projects.list(per_page=self.PER_PAGE):
                yield ProjectDTO(
                    external_id=project.id,
                    name=project.name,
                    path=project.path_with_namespace,
                    description=project.description,
                    created_at=project.created_at,
                    dependencies={
                        dep for dep in self._list_dependencies(project_id=project.id)
                    },
                )

    def _list_dependencies(self, project_id) -> Generator[DependencyDTO, None, None]:
        project = self._api.projects.get(project_id, lazy=True)
        for item in project.repository_tree():
            if item["name"] in self._registered_dependency_file_types:
                contents = project.repository_raw_blob(item["id"])
                parser = parser_provider.provide(item["name"])
                yield from parser.parse(from_file=item["name"], contents=str(contents))
        yield from ()
