# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aioextensions']

package_data = \
{'': ['*']}

install_requires = \
['uvloop']

setup_kwargs = {
    'name': 'aioextensions',
    'version': '20.8.1295702',
    'description': '',
    'long_description': '# Python Asyncio Extensions\n\n[![Documentation](https://img.shields.io/badge/Documentation-click_here!-green)](https://kamadorueda.github.io/aioextensions/)\n[![PyPI](https://img.shields.io/pypi/v/aioextensions)](https://pypi.org/project/aioextensions)\n[![Status](https://img.shields.io/pypi/status/aioextensions)](https://pypi.org/project/aioextensions)\n[![License](https://img.shields.io/pypi/l/aioextensions)](https://github.com/kamadorueda/aioextensions/blob/latest/LICENSE.md)\n[![Downloads](https://img.shields.io/pypi/dm/aioextensions)](https://pypi.org/project/aioextensions)\n',
    'author': 'Kevin Amado',
    'author_email': 'kamadorueda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kamadorueda/aioextensions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
