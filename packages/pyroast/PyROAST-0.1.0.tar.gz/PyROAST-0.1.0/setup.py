# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyROAST']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyroast',
    'version': '0.1.0',
    'description': 'Reserved name',
    'long_description': None,
    'author': 'Kamuish',
    'author_email': 'andremiguel952@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
