"""
Author:     David Walshe
Date:       02 August 2022
"""

from pytest import fixture, mark, raises

from tests.unit import UnitTest

from unity_utils.templates.template_factory import TemplateFactory, TemplateType, TemplateData
from unity_utils.templates.gitignore import CONTENT as GITIGNORE_CONTENT


class TestTemplateFactory(UnitTest):
    """Tests for TemplateFactory."""

    @mark.parametrize("type_, file_name, content", [
        (TemplateType.GITIGNORE, ".gitignore", GITIGNORE_CONTENT),
    ])
    def test_make(self, type_, file_name, content, tmp_path):
        # WHEN
        result = TemplateFactory.make(type_=type_, location=tmp_path)
        # THEN
        assert result.file_name == file_name
        assert result.content == content
        assert result.location == tmp_path

    def test_make_fail(self, tmp_path):
        # WHEN
        with raises(TypeError):
            TemplateFactory.make(type_="invalid", location=tmp_path)

    def test_make_gitignore(self, tmp_path):
        # WHEN
        result = TemplateFactory.make_gitignore(location=tmp_path)
        # THEN
        assert result.file_name == ".gitignore"
        assert result.content == GITIGNORE_CONTENT
        assert result.location == tmp_path


class TestTemplateData(UnitTest):
    """Tests the TemplateData class."""

    file_name = "test.txt"
    content = "test"

    @fixture
    def template_data(self, tmp_path) -> TemplateData:
        """Returns a TemplateData instance."""
        return TemplateData(file_name="test.txt", content="test", location=tmp_path)

    def test_file_path(self, template_data, tmp_path):
        # WHEN
        result = template_data.file_path
        # THEN
        assert result == tmp_path / self.file_name

    def test_create(self, template_data, tmp_path):
        # WHEN
        template_data.create()
        # THEN
        assert (tmp_path / self.file_name).exists()
