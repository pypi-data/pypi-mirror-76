# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['racli', 'racli.ractf', 'racli.ractf.helpers', 'racli.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['racli = racli.racli:cli']}

setup_kwargs = {
    'name': 'racli',
    'version': '2.0.8',
    'description': 'A command-line program for interacting with RACTF.',
    'long_description': None,
    'author': 'Ben Griffiths',
    'author_email': 'sendbenspam@yahoo.co.uk',
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
