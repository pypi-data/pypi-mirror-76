# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_prune']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['git-prune = git_prune.main:cli']}

setup_kwargs = {
    'name': 'git-prune',
    'version': '0.0.8',
    'description': 'Clean up your local git branches to match the remote with one command.',
    'long_description': '# git-prune\n\n![license](https://img.shields.io/github/license/mashape/apistatus.svg)\n![pythonver](https://img.shields.io/badge/python-3.5%2B-blue.svg)\n![git-prune-ver](https://img.shields.io/badge/version-0.0.8-lightgrey.svg)\n\nClean up your local git branches to match the remote with one command. This tool checks your remote location for current branches, compares this list against the local git branches, and gives you the option to remove all orphaned local branches.\n\n### Installation\n\n`pip3 install git-prune`\n\n### Usage\n\n`git-prune` -- Prunes local branches in the current working directory.\n\n`git-prune -d /Path/to/repository` -- Prunes local branches in the provided directory.\n',
    'author': 'Richard Soper',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rsoper/git-prune',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
