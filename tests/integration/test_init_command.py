"""
Author:     David Walshe
Date:       26 July 2022
"""

from .base import IntegrationTest

from unity_utils.constants import FOLDERS, FILES
from unity_utils.entry import app


class TestInitCommand(IntegrationTest):
    """Integration tests for 'init' command."""

    def test_init_command(self, cli_runner, tmp_path):
        """Test the 'init' command."""
        result = cli_runner.invoke(app, ["init", "--project-path", tmp_path])
        assert result.exit_code == 0
        assert result.output.find("Initialising Unity project") != -1
        assert result.output.find("Creating folders") != -1
        assert result.output.find("Creating files") != -1
        assert result.output.find("Renaming files") != -1
        assert result.output.find("Done") != -1

        for folder in FOLDERS:
            assert (tmp_path / folder).exists() == True
            assert (tmp_path / folder).is_dir() == True

        for file in FILES:
            assert (tmp_path / file).exists() == True
            assert (tmp_path / file).is_file() == True

        assert (tmp_path / "Assets" / "Scenes" / "Game.unity").exists() == True
