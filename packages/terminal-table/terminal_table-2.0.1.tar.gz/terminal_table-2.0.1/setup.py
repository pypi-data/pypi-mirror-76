# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminal_table']

package_data = \
{'': ['*']}

install_requires = \
['ansi-colours>=1.0.0,<2.0.0',
 'coverage>=5.2.1,<6.0.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'pytest>=6.0.1,<7.0.0']

setup_kwargs = {
    'name': 'terminal-table',
    'version': '2.0.1',
    'description': 'Print headers and rows of data in terminal',
    'long_description': None,
    'author': 'Sarcoma',
    'author_email': 'sean@orderandchaoscreative.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
