"""
Author:     David Walshe
Date:       31 July 2022
"""

import os

# ==============================================================================
# "./" files/folders
# ==============================================================================

_ROOT_FILES = [
    "README.md",
]

# ==============================================================================
# './Assets/' files/folers
# ==============================================================================

_ASSET_FOLDERS = [
    os.path.join("Assets", folder)
    for folder in ["Audio", "Docs", "Fonts", "Prefabs", "Scripts", "Scriptable_Objects", "Sprites"]
]

FOLDERS = [*_ASSET_FOLDERS]
FILES = [*_ROOT_FILES]
