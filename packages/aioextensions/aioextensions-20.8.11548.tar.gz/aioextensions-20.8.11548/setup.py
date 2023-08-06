# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aioextensions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aioextensions',
    'version': '20.8.11548',
    'description': '',
    'long_description': '# Aioextensions\n\n[![PyPI](https://img.shields.io/pypi/v/aioextensions)](https://pypi.org/project/aioextensions)\n[![Status](https://img.shields.io/pypi/status/aioextensions)](https://pypi.org/project/aioextensions)\n[![Downloads](https://img.shields.io/pypi/dm/aioextensions)](https://pypi.org/project/aioextensions)\n[![License](https://img.shields.io/pypi/l/aioextensions)](../LICENSE)\n',
    'author': 'Kevin Amado',
    'author_email': 'kamadorueda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kamadorueda/aioextensions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
