# Simple Changes

[![MPL](https://img.shields.io/github/license/UnscriptedVN/simplechanges)](LICENSE.txt)
![Python](https://img.shields.io/badge/python-2.7+-blue.svg)
[![PyPI version](https://badge.fury.io/py/simplechanges.svg)](https://pypi.org/project/simplechanges)

<!-- ![Tests](https://github.com/UnscriptedVN/simplechanges/workflows/Tests/badge.svg) -->

**Simple Changes** is a dead-simple changelog format that keeps track of changes and call them programmatically. The file format is dead-easy to follow, and you can use this package to parse the file and get information in the changelog. Simple Changes is used in Unscripted to parse the game's changelog and present the latest version information to players, but this library can be used anywhere.

## Requirements

- Python 2.7+
- Poetry package manager (for building)

## Getting started

### Quick Start: Install on PyPI

Simple Changes is bundled in Unscripted, but you can install it into your projects anywhere from PyPI with pip:

```
pip install simplechanges
```

### Install from source

To install Simple Changes from the source code, first clone the repository from GitHub via `git clone`. You'll also need to install Poetry. In the root of the source, run the following commands:

```
- poetry install
- poetry build
```

The resulting wheel files will be available in the dist directory.

## Syntax

- Comments are wrapped in `/*` and `*/`.
- Versions are denoted by square brackets: `[v1.0.0]`.
- Notes are denoted with dashes in the beginning and end with a newline.

> Note: To get the `latest` version to work in the parser, always place the latest version at the top of the file.

## Example file

```
/*
    Changelog Test
*/

[v1.0.1]
- Made a small bugfix.

[v1.0.0]
- Launched!
- I ate cheese.

```

## Usage

Using the package is relatively easy. To get the latest version in the changelog, assuming the changelog builds up:

```py
from simplechanges import SimpleChangesParser

changelog = SimpleChangesParser("changelog.changes")
changelog.parse()
version, notes = changelog.latest
```

After parsing, you also can browse for a specific version:

```py
from simplechanges import SimpleChangesParser

changelog = SimpleChangesParser("changelog.changes")
changelog.parse()
version, notes = changelog.versions["v1.0.0"]
```

## License

This code is licensed under the Mozilla Public License, v2.0.
