import json
import re
from re import Pattern
from typing import Generator

from dependency.dto import DependencyDTO
from dependency.parser.base import BaseParser
from project.models import ProjectDependency


class PackageLockJsonParser(BaseParser):
    _SOURCE_FILE_REGEX = re.compile("^package-lock.json$", re.IGNORECASE)
    _KEY_DEPENDENCIES = "dependencies"
    _KEY_VERSION = "version"
    _AT = "@"
    _EMPTY = ""

    @classmethod
    def parse(
        cls, source_file: str, contents: bytes
    ) -> Generator[DependencyDTO, None, None]:
        json_contents = json.loads(contents)
        dependencies: dict[str, dict] = json_contents.get(cls._KEY_DEPENDENCIES, {})
        return (
            DependencyDTO(
                name=name.replace(cls._AT, cls._EMPTY),
                version=dependency[cls._KEY_VERSION],
                source_file=source_file,
                source_type=str(ProjectDependency.SourceTypeChoices.PACKAGE_LOCK_JSON),
            )
            for name, dependency in dependencies.items()
        )

    @classmethod
    def source_file_regex(cls) -> Pattern:
        return cls._SOURCE_FILE_REGEX


class YarnLockParser(BaseParser):
    _SOURCE_FILE_REGEX = re.compile("^yarn.lock$", re.IGNORECASE)
    _REGEX = re.compile(r'^([\w\d\-]+)@.*\n\s+version "([\d.]+)"$', re.MULTILINE)
    _ENCODING = "utf-8"

    @classmethod
    def parse(
        cls, source_file: str, contents: bytes
    ) -> Generator[DependencyDTO, None, None]:
        return (
            DependencyDTO(
                name=dependency[1],
                version=dependency[2],
                source_file=source_file,
                source_type=str(ProjectDependency.SourceTypeChoices.YARN_LOCK),
            )
            for dependency in re.finditer(cls._REGEX, str(contents, cls._ENCODING))
        )

    @classmethod
    def source_file_regex(cls) -> Pattern:
        return cls._SOURCE_FILE_REGEX
