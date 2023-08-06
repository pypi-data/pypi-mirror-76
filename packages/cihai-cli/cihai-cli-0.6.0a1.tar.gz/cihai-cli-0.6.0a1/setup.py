# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cihai_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.12,<6', 'cihai>=0.9.0,<0.10.0', 'click>=7']

entry_points = \
{'console_scripts': ['cihai = cihai_cli.cli:cli']}

setup_kwargs = {
    'name': 'cihai-cli',
    'version': '0.6.0a1',
    'description': 'Command line frontend for the cihai CJK language library',
    'long_description': None,
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cihai-cli.git-pull.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
