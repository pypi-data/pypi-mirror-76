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
    'version': '0.1.1',
    'description': 'Cliente para comunicacion con flowAPI-3 de flow.cl',
    'long_description': 'PyFlowCL\n============\n\nCliente API para operaciones con el servicio de pagos Flow.cl  \n[FlowAPI-3.0.1](https://www.flow.cl/docs/api.html) \n\n---\n\n## Features\n- Currently the "[Payment](https://www.flow.cl/docs/api.html#tag/payment)" command is available\n\n\n---\n\n## Setup\nThis project is managed by Poetry (a requierements.txt file is also provided)\n\n---\n\n## Usage\n```python\nfrom pyflowcl import Payment\np = Payment.PaymentRequest()\np.set_env(pyflowcl.__sandbox__)\np.set_auth("token", "key")\np.get_payment_url(\'Payment\', 5000, Payment.CLP, Payment.ALL_METHODS)\nprint(p)\n```\n\n---\n\n## License\n>You can check out the full license [here](https://github.com/mariofix/pyflowcl/blob/stable-v3/LICENSE)\n\nThis project is licensed under the terms of the **MIT** license.  \nFlowAPI is licensed under the terms of the **Apache 2.0** license.\n',
    'author': 'Mario Hernandez',
    'author_email': 'yo@mariofix.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mariofix/pyflowcl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
