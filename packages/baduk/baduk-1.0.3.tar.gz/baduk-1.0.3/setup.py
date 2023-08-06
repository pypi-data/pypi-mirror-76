# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baduk',
 'baduk.action',
 'baduk.command',
 'baduk.constants',
 'baduk.dialog',
 'baduk.enums',
 'baduk.exception',
 'baduk.game',
 'baduk.service',
 'baduk.stones',
 'baduk.ui',
 'baduk.ui.action',
 'baduk.validation']

package_data = \
{'': ['*'], 'baduk': ['templates/*']}

install_requires = \
['ansi-colours==0.2.6', 'terminal-table==0.3.1', 'text-template==0.1.4']

entry_points = \
{'console_scripts': ['baduk = baduk.__main__:main']}

setup_kwargs = {
    'name': 'baduk',
    'version': '1.0.3',
    'description': 'Python Baduk Game',
    'long_description': None,
    'author': 'Sarcoma',
    'author_email': 'sean@orderandchaoscreative.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
