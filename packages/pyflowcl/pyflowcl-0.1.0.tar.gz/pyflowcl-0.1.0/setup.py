# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyflowcl']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'pyflowcl',
    'version': '0.1.0',
    'description': 'Cliente para comunicacion con API de flow.cl',
    'long_description': None,
    'author': 'Mario Hernandez',
    'author_email': 'yo@mariofix.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
