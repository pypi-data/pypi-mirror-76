# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temeco']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'temeco',
    'version': '0.1.2',
    'description': 'A small package handling telegram message copying preserving text entities',
    'long_description': None,
    'author': 'monomonedula',
    'author_email': 'valh@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monomonedula/temeco',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
