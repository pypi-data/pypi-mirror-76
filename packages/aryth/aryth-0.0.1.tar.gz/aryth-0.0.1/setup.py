# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aryth',
 'aryth.bound_matrix',
 'aryth.bound_vector',
 'aryth.enum_bound_keys',
 'aryth.math',
 'aryth.stat']

package_data = \
{'': ['*']}

install_requires = \
['intype>=0.0.2,<0.0.3', 'texting>=0.0.2,<0.0.3', 'veho>=0.0.2,<0.0.3']

setup_kwargs = {
    'name': 'aryth',
    'version': '0.0.1',
    'description': 'numerical tools',
    'long_description': '',
    'author': 'Hoyeung Wong',
    'author_email': 'hoyeungw@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hoyeungw/aryth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
