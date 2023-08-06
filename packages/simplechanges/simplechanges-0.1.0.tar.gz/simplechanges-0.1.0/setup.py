# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplechanges']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simplechanges',
    'version': '0.1.0',
    'description': 'A simple changelog parser',
    'long_description': '# Simple Changes\n\n[![MPL](https://img.shields.io/github/license/UnscriptedVN/simplechanges)](LICENSE.txt)\n![Python](https://img.shields.io/badge/python-2.7+-blue.svg)\n[![PyPI version](https://badge.fury.io/py/simplechanges.svg)](https://pypi.org/project/simplechanges)\n\n<!-- ![Tests](https://github.com/UnscriptedVN/simplechanges/workflows/Tests/badge.svg) -->\n\n**Simple Changes** is a dead-simple changelog format that keeps track of changes and call them programmatically. The file format is dead-easy to follow, and you can use this package to parse the file and get information in the changelog. Simple Changes is used in Unscripted to parse the game\'s changelog and present the latest version information to players, but this library can be used anywhere.\n\n## Requirements\n\n- Python 2.7+\n- Poetry package manager (for building)\n\n## Getting started\n\n### Quick Start: Install on PyPI\n\nSimple Changes is bundled in Unscripted, but you can install it into your projects anywhere from PyPI with pip:\n\n```\npip install simplechanges\n```\n\n### Install from source\n\nTo install Simple Changes from the source code, first clone the repository from GitHub via `git clone`. You\'ll also need to install Poetry. In the root of the source, run the following commands:\n\n```\n- poetry install\n- poetry build\n```\n\nThe resulting wheel files will be available in the dist directory.\n\n## Syntax\n\n- Comments are wrapped in `/*` and `*/`.\n- Versions are denoted by square brackets: `[v1.0.0]`.\n- Notes are denoted with dashes in the beginning and end with a newline.\n\n> Note: To get the `latest` version to work in the parser, always place the latest version at the top of the file.\n\n## Example file\n\n```\n/*\n    Changelog Test\n*/\n\n[v1.0.1]\n- Made a small bugfix.\n\n[v1.0.0]\n- Launched!\n- I ate cheese.\n\n```\n\n## Usage\n\nUsing the package is relatively easy. To get the latest version in the changelog, assuming the changelog builds up:\n\n```py\nfrom simplechanges import SimpleChangesParser\n\nchangelog = SimpleChangesParser("changelog.changes")\nchangelog.parse()\nversion, notes = changelog.latest\n```\n\nAfter parsing, you also can browse for a specific version:\n\n```py\nfrom simplechanges import SimpleChangesParser\n\nchangelog = SimpleChangesParser("changelog.changes")\nchangelog.parse()\nversion, notes = changelog.versions["v1.0.0"]\n```\n\n## License\n\nThis code is licensed under the Mozilla Public License, v2.0.\n',
    'author': 'Marquis Kurt',
    'author_email': 'software@marquiskurt.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UnscriptedVN/simplechanges',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
