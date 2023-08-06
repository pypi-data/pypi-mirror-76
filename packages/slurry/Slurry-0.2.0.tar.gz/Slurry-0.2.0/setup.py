# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurry']

package_data = \
{'': ['*']}

install_requires = \
['trio>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'slurry',
    'version': '0.2.0',
    'description': 'An async stream processing microframework',
    'long_description': '.. image:: https://img.shields.io/pypi/v/slurry.svg\n   :target: https://pypi.org/project/slurry\n   :alt: Latest PyPi version\n\n.. image:: https://travis-ci.com/andersea/slurry.svg?branch=master\n   :target: https://travis-ci.com/andersea/slurry\n   :alt: Build Status\n\nSlurry - An async stream processing microframework\n==================================================',
    'author': 'Anders Ellenshøj Andersen',
    'author_email': 'andersa@ellenshoej.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andersea/slurry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
