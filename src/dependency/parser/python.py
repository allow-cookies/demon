import json
import re
from typing import Generator

from dependency.dto import DependencyDTO
from dependency.parser.base import BaseParser


class RequirementsTxtParser(BaseParser):
    _REGEX = re.compile(r"([\d\w\-]+)==([\d\w.]+)", re.MULTILINE)
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
            )
            for dependency in re.finditer(cls._REGEX, str(contents, cls._ENCODING))
        )


class PipfileLockParser(BaseParser):
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
            )
            for name, dependency in dependencies.items()
        )
