from dependency.models import Dependency
from project.models import ProjectDependency


SOURCE_FILE_CHOICES = ProjectDependency.SourceTypeChoices
LANGUAGE_CHOICES = Dependency.DependencyLanguageChoices

SOURCE_FILE_LANGUAGE_MAP: dict[str, str] = {
    str(SOURCE_FILE_CHOICES.YARN_LOCK): str(LANGUAGE_CHOICES.JAVASCRIPT),
    str(SOURCE_FILE_CHOICES.PIPFILE_LOCK): str(LANGUAGE_CHOICES.PYTHON),
    str(SOURCE_FILE_CHOICES.PACKAGE_LOCK_JSON): str(LANGUAGE_CHOICES.JAVASCRIPT),
    str(SOURCE_FILE_CHOICES.REQUIREMENTS_TXT): str(LANGUAGE_CHOICES.PYTHON),
}
