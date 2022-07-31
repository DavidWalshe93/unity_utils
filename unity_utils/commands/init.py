"""
Author:     David Walshe
Date:       26 July 2022
"""

from pathlib import Path

from typer import Typer, secho
from typer.colors import BRIGHT_GREEN, BRIGHT_RED, BRIGHT_YELLOW

app = Typer()


class ProjectInitializer:
    """Helper class to initialise a new Unity project."""

    def __init__(self, root_path: Path):
        """Class constructor."""
        self.root_path = root_path

    def create_folder(self, folder: str):
        """
        Create a folder if it does not exist.
        :param folder: The folder to create.
        :return: The path to the folder.
        """
        folder_path = self.root_path / folder
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
            secho(f"'{folder_path}' created.", fg=BRIGHT_GREEN)
        else:
            secho(f"'{folder_path}' already exists.", fg=BRIGHT_YELLOW)

    def create_file(self, file: str):
        """
        Create a file if it does not exist.
        :param file: The file to create.
        :return: The path to the file.
        """
        file_path = self.root_path / file
        if not file_path.exists():
            file_path.touch()
            secho(f"'{file_path}' created.", fg=BRIGHT_GREEN)
        else:
            secho(f"'{file_path}' already exists.", fg=BRIGHT_YELLOW)

    def rename_file(self, file: str, new_file: str):
        """
        Rename a file.
        :param file: The file to rename.
        :param new_file: The new name for the file.
        :return: The path to the file.
        """
        file_path = self.root_path / file
        new_file_path = self.root_path / new_file
        print(file_path, new_file_path)
        if file_path.exists():
            file_path.rename(new_file_path)
            secho(f"'{file_path}' renamed to '{new_file_path}'.", fg=BRIGHT_GREEN)
        else:
            secho(f"'{file_path}' does not exist.", fg=BRIGHT_RED)
