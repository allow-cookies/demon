import logging
import re
from typing import Generator, Pattern, Type
from uuid import UUID

import gitlab
from gitlab import GitlabGetError

from connector.base import PlatformConnector
from dependency.dto import DependencyDTO
from dependency.parser.base import BaseParser
from dependency.parser.provider import parser_provider
from project.dto import ProjectDTO
from project.models import Project
from user_platform.models import UserPlatform


class GitLabConnector(PlatformConnector):
    _VISIBILITY = "private"
    _FIELD_NAME = "name"
    _FIELD_ID = "id"

    def __init__(self, user_id: UUID):
        super().__init__(user_id=user_id)
        url, token = self._fetch_credentials(user_id)
        self._api = gitlab.Gitlab(url, private_token=token)
        self._parsers_regex_map: dict[Type[BaseParser], Pattern] = {
            parser: parser.source_file_regex() for _, parser in parser_provider.all().items()
        }

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
        for project in self._api.projects.list(visibility=self._VISIBILITY, all=True):
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
        try:
            for item in project.repository_tree(recursive=True, all=True):
                file_name = item[self._FIELD_NAME]
                for parser, pattern in self._parsers_regex_map.items():
                    if re.fullmatch(pattern, file_name) is not None:
                        contents = project.repository_raw_blob(item[self._FIELD_ID])
                        yield from parser.parse(source_file=file_name, contents=contents)
        except GitlabGetError:
            logging.info(f"Repository tree for project {project_id} not found")
        yield from ()
