"""Base test structure for Integration tests."""

from pytest import fixture
from typer.testing import CliRunner

from tests import BaseTest


class IntegrationTest(BaseTest):
    """Base test structure for Integration tests."""

    @fixture
    def new_project_setup(self, tmp_path):
        """Set up a stock Unity Project directory structure."""
        scenes = tmp_path / "Assets" / "Scenes"

        scenes.mkdir(exist_ok=True, parents=True)
        (scenes / "SampleScene.unity").touch()

    @fixture
    def cli_runner(self, new_project_setup) -> CliRunner:
        """Return a CliRunner instance."""
        return CliRunner()

