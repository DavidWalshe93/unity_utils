"""
Author:     David Walshe
Date:       02 August 2022
"""

from enum import Enum
from typing import NamedTuple
from pathlib import Path

# Templates
from unity_utils.templates.gitignore import content as gitignore_content


class TemplateType(Enum):
    """Enum for the different types of templates."""
    GITIGNORE = "gitignore"


class TemplateData(NamedTuple):
    """
    Data to be used to generate a template.
    """
    file_name: str
    content: str
    location: Path

    @property
    def file_path(self) -> Path:
        """Returns the file path for the template."""
        return self.location / self.file_name

    def create(self):
        """
        Create the template file with a given file_name and content.
        :return: The path to the template file.
        """
        self.file_path.write_text(self.content)


class TemplateFactory:

    @classmethod
    def make(cls, type_: TemplateType, location: Path) -> TemplateData:
        """Factory method to create a template of a given type."""
        if not isinstance(type_, TemplateType):
            raise TypeError(f"Expected TemplateType, got {type(type_)}")

        return {
            TemplateType.GITIGNORE: cls.make_gitignore,
        }.get(type_)(location)

    @classmethod
    def make_gitignore(cls, location: Path) -> TemplateData:
        """Factory method to create a gitignore template."""
        return TemplateData(file_name=".gitignore", content=gitignore_content, location=location)
