# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frattlesnake']

package_data = \
{'': ['*']}

install_requires = \
['pyjnius>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'frattlesnake',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Samuel Gaus',
    'author_email': 'sam@gaus.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
