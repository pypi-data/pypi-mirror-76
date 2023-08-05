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
    'version': '0.1.10',
    'description': 'Modernizing FRC Data Analytics',
    'long_description': "Statbotics API\n==============\n\nStatbotics.io aims to modernize FRC data analytics through developing and distributing cutting-edge metrics and analysis. This Python API makes historical Elo and OPR statistics just a few Python lines away! Currently we support queries on teams, years, events, and matches. Read below for usage and documentation.\n\nVisit https://statbotics.io for more content!\n\nUsage\n-----\n\nWith Python>=3.6 and pip installed, run\n\n```\npip install statbotics\n```\n\nThen in a Python file, create a Statbotics object and get started!\n\n```\nimport statbotics\n\nsb = statbotics.Statbotics()\nprint(sb.getTeam(254))\n\n>> {'team':254, 'name': 'The Cheesy Poofs', 'state': 'CA', 'country': 'USA', 'district': 'None',\n    'active': True, 'elo': 1860, 'elo_recent': 1972, 'elo_mean': 1898, 'elo_max': 2145}\n```\n\nRead below for more methods!\n\nAPI Reference\n-------------\n\nVisit https://statbotics.readthedocs.io/en/latest/\n\nContribute\n----------\n\nIf you are interested in contributing, reach out to Abhijit Gupta (avgupta456@gmail.com)\n\nSupport\n-------\n\nIf you are having issues, please let us know. We welcome issues and pull requests.\n\nLicense\n-------\n\nThe project is licensed under the MIT license.\n",
    'author': 'Abhijit Gupta',
    'author_email': 'avgupta456@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://statbotics.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
