# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wgadmin', 'wgadmin.subcommands']

package_data = \
{'': ['*'], 'wgadmin': ['templates/*']}

install_requires = \
['argcomplete>=1.12.0,<2.0.0', 'jinja2==2.11.2']

entry_points = \
{'console_scripts': ['wgadmin = wgadmin.main:main']}

setup_kwargs = {
    'name': 'wgadmin',
    'version': '0.1.0',
    'description': '',
    'long_description': '# wgadmin\n\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n',
    'author': 'Fabian Köhler',
    'author_email': 'fkoehler@physnet.uni-hamburg.de',
    'maintainer': 'Fabian Köhler',
    'maintainer_email': 'fkoehler@physnet.uni-hamburg.de',
    'url': 'https://github.com/f-koehler/wgadmin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
