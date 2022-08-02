# Unity Utils

---

![Build](https://github.com/DavidWalshe93/unity_utils/actions/workflows/cicd.yml/badge.svg)
[![codecov](https://codecov.io/gh/DavidWalshe93/unity_utils/branch/main/graph/badge.svg?token=M2L84RI4KE)](https://codecov.io/gh/DavidWalshe93/unity_utils)
![GitHub](https://img.shields.io/github/license/mashape/apistatus)

## Overview

---

The project contains a CLI tool with some helpful tools for working with Unity Projects.

## Requirements

---

### Make

You will need `make` to run the various `make` automation targets.

**Windows Users** should look at [GnuWin32 Make](http://gnuwin32.sourceforge.net/packages/make.htm).

## Setup

---

1) Clone the project.
2) Open a terminal (`GitBash` for Windows Users)
3) `cd <PATH_TO_CLONED_REPO>/unity-utils`
4) `make test`  <--- Verify everything works.
5) `make build` <--- Build the project and install `unity-utils` as a terminal command.

## Commands

---

### init

`ìnit` is used to bootstrap a new Unity project to create the following structure

```
UnityProject/
    Assets/
        Audio/
        Docs/
        Fonts/
        Scripts/
        Sprites/
        Scenes/
            Game.unity
    .gitignore
    README.md
```

The above file structure is a typical starting point for most new project. To keep projects
structures similar between projects, the `init` command sets up a repeatable structure. This is
handy for beginners or those working on various small projects starting out with Unity.


