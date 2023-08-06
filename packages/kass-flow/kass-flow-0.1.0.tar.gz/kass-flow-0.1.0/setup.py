# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kass_flow']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'kass-flow',
    'version': '0.1.0',
    'description': 'Send payments to the KASS mobile payment service',
    'long_description': None,
    'author': 'Jón Levy',
    'author_email': 'nonni@nonni.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
