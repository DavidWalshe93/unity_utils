"""
Author:     David Walshe
Date:       26 July 2022
"""

import sys
from pathlib import Path
import toml

from typer import Option, Typer, secho
from typer.colors import BRIGHT_CYAN, BRIGHT_GREEN

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from unity_utils.constants import FOLDERS, FILES

from unity_utils.commands.init import (  # pylint: disable=wrong-import-position # noqa: E402
    ProjectInitializer,
)

app = Typer()


@app.command(name="version")
def version():
    """Print the version number."""
    from unity_utils.version import VERSION
    secho(f"{VERSION}", fg=BRIGHT_CYAN)


@app.command(name="init")
def init_unity_project(
        project_path: Path = Option(
            ...,
            "-p",
            "--project-path",
            help="The path to the project to initialize. Defaults the the current working directory.",
        )
):
    """Initialise a new Unity project with Folder/Files and Naming Conventions."""
    secho(f"Initialising Unity project in '{project_path}'...", fg=BRIGHT_CYAN)
    initializer = ProjectInitializer(project_path)

    secho("Creating folders...", fg=BRIGHT_CYAN)
    _ = [initializer.create_folder(folder) for folder in FOLDERS]

    secho("Creating files...", fg=BRIGHT_CYAN)
    _ = [initializer.create_file(file) for file in FILES]

    secho("Renaming files...", fg=BRIGHT_CYAN)
    initializer.rename_file("Assets/Scenes/DefaultScene.unity", "Assets/Scenes/Game.unity")

    secho("Done.", fg=BRIGHT_GREEN)


if __name__ == "__main__":  # pragma: no cover
    app()
