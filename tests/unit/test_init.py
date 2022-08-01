"""
Author:     David Walshe
Date:       26 July 2022
"""
from pathlib import Path

from pytest import fixture, mark

from .base import UnitTest

from unity_utils.constants import FOLDERS, FILES
from unity_utils.commands.init import ProjectInitializer


class TestProjectInitializer(UnitTest):
    """"Tests for ProjectInitializer class."""

    @fixture
    def project_initializer(self, tmp_path) -> ProjectInitializer:
        """Returns a ProjectInitializer instance."""
        return ProjectInitializer(tmp_path)

    @mark.parametrize("folder", FOLDERS)
    def test_create_folder(self, folder, project_initializer):
        """Test the create_folder method."""
        project_initializer.create_folder(folder)
        assert (project_initializer.root_path / folder).exists() == True
        assert (project_initializer.root_path / folder).is_dir() == True

    @mark.parametrize("folder", FOLDERS)
    def test_create_folder_fail(self, folder, project_initializer, capsys):
        """Test the create_folder method."""
        path = Path(project_initializer.root_path / folder)
        assert path.exists() == False
        path.mkdir(parents=True)
        Path(project_initializer.root_path / folder).mkdir(exist_ok=True)
        project_initializer.create_folder(folder)

        captured = capsys.readouterr()
        assert captured.out.find("already exists") != -1

    @mark.parametrize("file", FILES)
    def test_create_file(self, file, project_initializer):
        """Test the create_file method."""
        project_initializer.create_file(file)
        assert (project_initializer.root_path / file).exists()

    @mark.parametrize("file", FILES)
    def test_create_file_fail(self, file, project_initializer, capsys):
        """Test the create_file method."""
        path = Path(project_initializer.root_path / file)
        assert path.exists() == False
        path.touch(exist_ok=True)
        project_initializer.create_file(file)

        captured = capsys.readouterr()
        assert captured.out.find("already exists") != -1

    def test_rename_file(self, project_initializer, tmp_path):
        """Test the rename_file method."""
        before_file_part = "TestFolder/DefaultScene.unity"
        before_file = tmp_path / "TestFolder" / "DefaultScene.unity"
        after_file_part = "TestFolder/Game.unity"

        Path(before_file.parent).mkdir(parents=True, exist_ok=True)
        before_file.touch()

        assert (project_initializer.root_path / before_file_part).exists()
        assert (project_initializer.root_path / after_file_part).exists() == False
        project_initializer.rename_file(before_file_part, after_file_part)
        assert (project_initializer.root_path / before_file_part).exists() == False
        assert (project_initializer.root_path / after_file_part).exists()

    def test_rename_file_fail(self, project_initializer, tmp_path, capsys):
        """Test the rename_file method."""
        before_file_part = "TestFolder/DefaultScene.unity"
        before_file = tmp_path / "TestFolder" / "DefaultScene.unity"
        after_file_part = "TestFolder/Game.unity"

        Path(before_file.parent).mkdir(parents=True, exist_ok=True)

        assert (project_initializer.root_path / before_file_part).exists() == False
        assert (project_initializer.root_path / after_file_part).exists() == False
        project_initializer.rename_file(before_file_part, after_file_part)

        captured = capsys.readouterr()
        assert captured.out.find(" does not exist") != -1

    def test_fail(self):
        assert False