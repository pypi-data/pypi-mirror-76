# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statbotics']

package_data = \
{'': ['*']}

install_requires = \
['cachecontrol>=0.12.6,<0.13.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'statbotics',
    'version': '0.1.9',
    'description': 'Modernizing FRC Data Analytics',
    'long_description': None,
    'author': 'Abhijit Gupta',
    'author_email': 'avgupta456@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
