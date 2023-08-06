# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mako2cli']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'click>=7.1.2,<8.0.0',
 'mako>=1.1.3,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

entry_points = \
{'console_scripts': ['m2cli = mako2cli.cli:main']}

setup_kwargs = {
    'name': 'mako2cli',
    'version': '0.1.0',
    'description': 'Mako Template Command-Line Tool',
    'long_description': '[![Tests](https://github.com/leaningdiggers/mako2cli/workflows/Tests/badge.svg)](https://github.com/leaningdiggers/mako2cli/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/leaningdiggers/mako2cli/branch/master/graph/badge.svg)](https://codecov.io/gh/leaningdiggers/mako2cli)\n\n# mako2cli\n\nThis project aims to port Mako Template to a simple usage on command line\n\n## Installation\n\nTo install the mako2cli Python project,\nrun this command in your terminal:\n\n```\n$ pip install mako2cli\n```\n',
    'author': 'fbagagli',
    'author_email': 'francesco.bagagli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fbagagli/mako2cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
