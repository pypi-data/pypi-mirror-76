# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spammer_py']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'spammer-py',
    'version': '0.1.3',
    'description': 'Computer and email spammer',
    'long_description': None,
    'author': 'AndyZhou',
    'author_email': 'AndyForever0108@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
