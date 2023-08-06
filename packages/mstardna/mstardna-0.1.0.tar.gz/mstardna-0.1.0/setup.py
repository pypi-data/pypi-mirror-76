# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mstardna']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.42,<2.0.0', 'pandas>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'mstardna',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jinyoung Kim',
    'author_email': 'jinyoung.kim@morningstar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
