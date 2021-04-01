import json
import re
from typing import Generator, Pattern

from dependency.dto import DependencyDTO
from dependency.parser.base import BaseParser
from project.models import ProjectDependency


class RequirementsTxtParser(BaseParser):
    _SOURCE_FILE_REGEX = re.compile(r"^\w+.txt$", re.IGNORECASE)
    _REGEX = re.compile(r"([\d\w\-]+)==([\d\w.]+)", re.MULTILINE)
    _ENCODING = "utf-8"

    @classmethod
    def parse(
        cls, source_file: str, contents: bytes
    ) -> Generator[DependencyDTO, None, None]:
        try:
            for dependency in re.finditer(cls._REGEX, str(contents, cls._ENCODING)):
                yield DependencyDTO(
                    name=dependency[1],
                    version=dependency[2],
                    source_file=source_file,
                    source_type=str(ProjectDependency.SourceTypeChoices.REQUIREMENTS_TXT),
                )
        except UnicodeDecodeError:
            yield from ()

    @classmethod
    def source_file_regex(cls) -> Pattern:
        return cls._SOURCE_FILE_REGEX


class PipfileLockParser(BaseParser):
    _SOURCE_FILE_REGEX = re.compile(r"^pipfile.lock$", re.IGNORECASE)
    _KEY_DEFAULT = "default"
    _KEY_DEVELOP = "develop"
    _KEY_VERSION = "version"
    _EXACT = "=="
    _EMPTY = ""

    @classmethod
    def parse(
        cls, source_file: str, contents: bytes
    ) -> Generator[DependencyDTO, None, None]:
        json_contents = json.loads(contents)
        dependencies: dict[str, dict] = {
            **json_contents.get(cls._KEY_DEFAULT, {}),
            **json_contents.get(cls._KEY_DEVELOP, {}),
        }
        return (
            DependencyDTO(
                name=name,
                version=dependency[cls._KEY_VERSION].replace(cls._EXACT, cls._EMPTY),
                source_file=source_file,
                source_type=str(ProjectDependency.SourceTypeChoices.PIPFILE_LOCK)
            )
            for name, dependency in dependencies.items()
        )

    @classmethod
    def source_file_regex(cls) -> Pattern:
        return cls._SOURCE_FILE_REGEX
