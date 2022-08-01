"""
Author:     David Walshe
Date:       31 July 2022
"""

from pathlib import Path
import toml

PYPROJECT_TOML_PATH = Path(__file__).parent.parent / "pyproject.toml"


def text(version: str):
    """
    Returns formatted text.
    :param version: The text to print.
    """
    return f'"""THIS FILE IS AUTO-GENERATED"""\nVERSION = "{version}"\n'


if __name__ == '__main__':
    parsed_toml = toml.load(PYPROJECT_TOML_PATH)
    cli_version = parsed_toml["tool"]["poetry"]["version"]
    version_file = Path(parsed_toml["build"]["cli"]["version_file"]).absolute()

    version_file.write_text(text(cli_version))
