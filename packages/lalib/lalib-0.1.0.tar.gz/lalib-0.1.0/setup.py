# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lalib']

package_data = \
{'': ['*']}

extras_require = \
{':python_version == "3.7"': ['importlib_metadata>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'lalib',
    'version': '0.1.0',
    'description': 'A library in core Python to study linear algebra',
    'long_description': "# `lalib` - A library to study linear algebra\n\nThe goal of this project is\nto create a library written solely in core [Python](https://docs.python.org/3/)\n    (incl. the [standard library](https://docs.python.org/3/library/index.html))\nto learn about [linear algebra](https://en.wikipedia.org/wiki/Linear_algebra).\n\n[![PyPI](https://img.shields.io/pypi/v/lalib.svg)](https://pypi.org/project/lalib/)\n[![Tests](https://github.com/webartifex/lalib/workflows/Tests/badge.svg)](https://github.com/webartifex/lalib/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/webartifex/lalib/branch/main/graph/badge.svg)](https://codecov.io/gh/webartifex/lalib)\n\n\n## Contributing & Development\n\n\n### Local Develop Environment\n\nGet a copy of this repository:\n\n`git clone git@github.com:webartifex/lalib.git`\n\nWhile `lalib` comes without any dependencies except core Python\n    and the standard library for the user,\nwe assume a couple of mainstream packages to be installed\nto ensure code quality during development.\nThese can be viewed in the [pyproject.toml](pyproject.toml) file.\n\nTo replicate the project maintainer's develop environment,\ninstall the pinned dependencies from the [poetry.lock](poetry.lock) file\nwith the [poetry](https://python-poetry.org/docs/) dependency manager:\n\n`poetry install`\n\nThis automatically creates and uses a [virtual environment](https://docs.python.org/3/tutorial/venv.html).\n\n\n### Testing & Maintenance Tasks\n\nWe use [nox](https://nox.thea.codes/en/stable/) to run the test suite\n    in an isolated environment\nand to invoke the prepared maintenance tasks during development\n(`nox` is quite similar to [tox](https://tox.readthedocs.io/en/latest/)).\nIt is configured in the [noxfile.py](noxfile.py) file.\n\nTo list all available tasks, called sessions in `nox`, simply run:\n\n`poetry run nox --list`\n\nTo execute all sessions that the CI server would run, invoke:\n\n`poetry run nox`\n\nThat runs the test suite for all supported Python versions.\n\n\n#### Code Formatting & Linting\n\nWe follow [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html)\nand include [type hints](https://docs.python.org/3/library/typing.html) where possible.\n\nDuring development, `poetry run nox -s format` and `poetry run nox -s lint` may\n    be helpful.\n\nThe first task formats all source code files with\n    [autoflake](https://pypi.org/project/autoflake/),\n    [black](https://pypi.org/project/black/), and\n    [isort](https://pypi.org/project/isort/).\n`black` keeps single quotes `'` unchanged to minimize visual noise\n    (single quotes are enforced by `wemake-python-styleguide`; see next).\n\nThe second task lints all source code files with\n    [flake8](https://pypi.org/project/flake8/),\n    [mypy](https://pypi.org/project/mypy/), and\n    [pylint](https://pypi.org/project/pylint/).\n`flake8` is configured with a couple of plug-ins,\nmost notably [wemake-python-styleguide](https://wemake-python-stylegui.de/en/latest/).\n\nYou may want to install the local [pre-commit](https://pre-commit.com/) hooks\n    that come with the project:\n\n`poetry run nox -s init-project`\n\nThat automates the formatting and linting before every commit.\nAlso, the test suite is run before every merge.\n\n\n### Branching Strategy\n\nThe branches in this repository follow the [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) model.\nIt is assumed that a feature branch is rebased *before* it is merged into `develop`.\nWhereas after a rebase a simple fast-forward merge is possible,\nall merges are made with explicit and *empty* merge commits\n(i.e., the merge itself does *not* change a single line of code).\nThis ensures that past branches remain visible in the logs,\nfor example, with `git log --graph`.\n",
    'author': 'Alexander Hess',
    'author_email': 'alexander@webartifex.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/webartifex/lalib',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
