# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rayycli', 'rayycli.ractf', 'rayycli.ractf.helpers', 'rayycli.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['rayycli = rayycli.rayycli:cli']}

setup_kwargs = {
    'name': 'rayycli',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
