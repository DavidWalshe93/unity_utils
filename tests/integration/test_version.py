"""
Author:     David Walshe
Date:       31 July 2022
"""

from unittest.mock import PropertyMock

from pytest import fixture
from pytest_mock import MockerFixture

from . import IntegrationTest

from unity_utils import entry
from unity_utils.entry import app, version
from unity_utils import version


class TestVersion(IntegrationTest):
    """Tests for version command."""

    def test_version_command(self, cli_runner, mocker: MockerFixture, monkeypatch):
        # GIVEN
        monkeypatch.setattr(version, "VERSION", "99.99.99")
        # WHEN
        result = cli_runner.invoke(app, ["version"])
        # THEN
        assert result.exit_code == 0
        assert result.output.find("99.99.99") != -1
